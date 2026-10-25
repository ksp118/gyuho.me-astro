#!/usr/bin/env bash
# 지정한 release로 current를 되돌림.  사용: ./scripts/rollback.sh <시각>
#                                     인자 없이 실행하면 release 목록만 출력
set -euo pipefail

ROOT=/srv/gyuho.me
CUR=$(readlink "$ROOT/current" 2>/dev/null || true)   # 예: releases/20261025-145119

if [[ $# -ne 1 ]]; then
  for d in "$ROOT"/releases/*/; do
    name=$(basename "$d")
    if [[ "releases/$name" == "$CUR" ]]; then echo "* $name"; else echo "  $name"; fi
  done
  exit 1
fi

TS=$1
if [[ ! "$TS" =~ ^[0-9]{8}-[0-9]{6}$ ]]; then echo "bad name: $TS" >&2; exit 1; fi
if [[ ! -f "$ROOT/releases/$TS/index.html" ]]; then echo "no such release: $TS" >&2; exit 1; fi
if [[ "releases/$TS" == "$CUR" ]]; then echo "already current: $TS"; exit 0; fi

ln -sfn "releases/$TS" "$ROOT/current.tmp"
mv -T "$ROOT/current.tmp" "$ROOT/current"
echo "rolled back: ${CUR#releases/} -> $TS"