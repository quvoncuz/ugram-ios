#!/usr/bin/env python3
"""Prepare the pinned Telegram checkout for a locally signed iPhone preview."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def credentials():
    api_id = os.environ.get('TELEGRAM_API_ID', '')
    api_hash = os.environ.get('TELEGRAM_API_HASH', '')
    if not re.fullmatch(r'[1-9][0-9]*', api_id) or api_id in {'4', '6'}:
        raise SystemExit('Set your own TELEGRAM_API_ID repository secret from my.telegram.org/apps.')
    if not re.fullmatch(r'[0-9a-fA-F]{32}', api_hash):
        raise SystemExit('Set TELEGRAM_API_HASH repository secret (32 hexadecimal characters).')
    return api_id, api_hash


def replace_exact(text, old, new, count=1):
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f'Upstream layout changed: expected {count} occurrences, found {actual}.')
    return text.replace(old, new)


def prepare(source):
    api_id, api_hash = credentials()
    pin = json.loads((ROOT / 'upstream.json').read_text())
    head = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if head != pin['ref']:
        raise SystemExit('Source commit differs from upstream.json; refusing to patch it.')
    version = json.loads((source / 'versions.json').read_text())
    if version['xcode'] != pin['xcode']:
        raise SystemExit('Source Xcode requirement differs from upstream.json.')
    build_path = source / 'Telegram/BUILD'
    bazelrc_path = source / '.bazelrc'
    build = build_path.read_text()
    # Two plist fragments supply the primary display name.
    build = replace_exact(build,
        '<key>CFBundleDisplayName</key>\n    <string>Telegram</string>',
        '<key>CFBundleDisplayName</key>\n    <string>Ugram Preview</string>', count=2)
    build = replace_exact(build,
        '    app_icons = [ ":{}_icon".format(name) for name in composer_icon_folders ],',
        '    app_icons = glob(["UgramAssets.xcassets/AppIcon.appiconset/*"]),')
    config = {
        'bundle_id': pin['bundle_id'], 'api_id': api_id, 'api_hash': api_hash,
        # This is a placeholder for an UNSIGNED build, not an Apple certificate.
        # The user's actual team is supplied later by the local sideloader.
        'team_id': '0000000000',
        'is_internal_build': 'true', 'is_appstore_build': 'false',
        'appstore_id': '0', 'app_specific_url_scheme': 'ugram',
        'premium_iap_product_id': '', 'enable_siri': False, 'enable_icloud': False,
    }
    flags = (
        '\n# Ugram: create a device archive for subsequent local signing.\n'
        'build --//Telegram:disableExtensions\n'
        'build --//Telegram:disableProvisioningProfiles\n'
        'build --features=disable_legacy_signing\n'
        'build --jobs=3\n'
    )
    bazelrc = bazelrc_path.read_text()
    if '# Ugram:' in bazelrc:
        raise SystemExit('Source is already prepared; use a fresh checkout for each build.')
    build_path.write_text(build)
    bazelrc_path.write_text(bazelrc + flags)
    config_path = source / 'build-system/ugram-configuration.json'
    config_path.write_text(json.dumps(config, indent=2) + '\n')
    config_path.chmod(0o600)
    print('Pinned source prepared; API credentials were not printed.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', type=Path)
    parser.add_argument('--check-credentials', action='store_true')
    args = parser.parse_args()
    if args.check_credentials:
        credentials()
        print('Telegram API secrets are present and have the expected format.')
    elif args.source:
        prepare(args.source.resolve())
    else:
        parser.error('Provide the Telegram checkout path or --check-credentials.')


if __name__ == '__main__':
    main()
