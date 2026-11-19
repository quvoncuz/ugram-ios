#!/usr/bin/env python3
"""Apply the human-readable, pinned Ugram feature patch before compilation."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def apply_features(source):
    patch = ROOT / 'ugram.patch'
    subprocess.run(['git', '-C', str(source), 'apply', '--check', str(patch)], check=True)
    subprocess.run(['git', '-C', str(source), 'apply', str(patch)], check=True)
    print('Ugram feature patch applied.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    apply_features(args.source.resolve())
