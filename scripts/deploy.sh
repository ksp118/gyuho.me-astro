#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

ROOT=/srv/gyuho.me
TS=$(date +%Y%m%d-%H%M%S)
DEST="$ROOT/releases/$TS"

if [[ ! -d "$ROOT/releases" ]]; then echo "missing: $ROOT/releases" >&2; exit 1; fi
if [[ -e "$DEST" ]]; then echo "already exists: $DEST" >&2; exit 1; fi

npm run build
if [[ ! -f dist/index.html ]]; then echo "build output missing" >&2; exit 1; fi

cp -r dist "$DEST"
ln -sfn "releases/$TS" "$ROOT/current.tmp"
mv -T "$ROOT/current.tmp" "$ROOT/current"
echo "deployed: $TS"