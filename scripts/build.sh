#!/usr/bin/env bash
set -euo pipefail

UGRAM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UGRAM_SOURCE="$(cd "${1:?Pass the prepared Telegram-iOS checkout}" && pwd)"
if [[ "$(uname -s)" != Darwin ]]; then
  echo 'Build requires the GitHub macOS runner; Linux is used for editing and sideloading.' >&2
  exit 1
fi

cd "$UGRAM_SOURCE"
python3 -u build-system/Make/Make.py \
  build \
  --configurationPath=build-system/ugram-configuration.json \
  --xcodeManagedCodesigning \
  --configuration=release_arm64 \
  --buildNumber="${GITHUB_RUN_NUMBER:-1}"

python3 "$UGRAM_ROOT/scripts/package.py" \
  "$UGRAM_SOURCE/bazel-bin/Telegram/Telegram.ipa" "$UGRAM_ROOT/out"
