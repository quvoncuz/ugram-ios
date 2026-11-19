#!/usr/bin/env python3
"""Validate a device IPA and embed ad-hoc entitlements for local re-signing."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def package(ipa, output):
    pin = json.loads((ROOT / 'upstream.json').read_text())
    if not ipa.is_file():
        raise SystemExit('Build did not produce Telegram.ipa.')
    with zipfile.ZipFile(ipa) as archive:
        infos = [n for n in archive.namelist() if n.startswith('Payload/')
                 and n.endswith('.app/Info.plist') and n.count('/') == 2]
        if len(infos) != 1:
            raise SystemExit('Expected exactly one main app in the IPA.')
        info = plistlib.loads(archive.read(infos[0]))
        if info.get('CFBundleIdentifier') != pin['bundle_id']:
            raise SystemExit('Unexpected app identity in IPA.')
        if 'iPhoneOS' not in info.get('CFBundleSupportedPlatforms', []):
            raise SystemExit('Simulator output cannot be installed on an iPhone.')
        if any('/PlugIns/' in n or '/Watch/' in n for n in archive.namelist()):
            raise SystemExit('Preview must not include extensions or Watch apps.')
    output.mkdir(parents=True, exist_ok=True)
    destination = output / 'Ugram-preview.ipa'
    with tempfile.TemporaryDirectory(prefix='ugram-ipa-') as temp:
        temp = Path(temp)
        # ditto preserves bundle symlinks and permissions.
        subprocess.run(['ditto', '-x', '-k', str(ipa.resolve()), str(temp)], check=True)
        app = temp / infos[0].removesuffix('/Info.plist')
        entitlements = temp / 'sideload.entitlements'
        entitlements.write_bytes(plistlib.dumps({
            'application-identifier': '0000000000.' + pin['bundle_id'],
            'com.apple.security.application-groups': ['group.' + pin['bundle_id']],
        }))
        # A '-' signature uses no Apple account or certificate. The IPA still needs
        # iloader/SideStore signing before installation on a physical iPhone.
        frameworks = app / 'Frameworks'
        if frameworks.exists():
            for framework in sorted(frameworks.iterdir()):
                if framework.suffix in {'.framework', '.dylib'}:
                    subprocess.run(['codesign', '--force', '--sign', '-', '--timestamp=none',
                                    str(framework)], check=True)
        subprocess.run(['codesign', '--force', '--sign', '-', '--timestamp=none',
                        '--entitlements', str(entitlements), str(app)], check=True)
        subprocess.run(['ditto', '-c', '-k', '--keepParent', str(temp / 'Payload'),
                        str(destination.resolve())], check=True)
    with destination.open('rb') as built_file:
        digest = hashlib.file_digest(built_file, 'sha256').hexdigest()
    (output / 'SHA256SUMS').write_text(digest + '  Ugram-preview.ipa\n')
    (output / 'build-info.json').write_text(json.dumps({
        'upstream_commit': pin['ref'], 'upstream_tag': pin['tag'],
        'build_number': os.environ.get('GITHUB_RUN_NUMBER', '1'),
        'bundle_id': pin['bundle_id'], 'sha256': digest,
        'signing': 'ad-hoc placeholder; requires local Apple-account re-signing',
        'ugram_android_features_ported': False,
    }, indent=2) + '\n')
    print('Device IPA packaged for local re-signing.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ipa', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    package(args.ipa, args.output)
