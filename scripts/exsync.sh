#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Ensure venv exists
if [[ ! -f ".venv/bin/activate" ]]; then
  echo "ERROR: .venv not found at $ROOT/.venv. Create it before running exsync." 1>&2
  exit 1
fi

# Activate venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[exsync 1/4] git pull --rebase"
git pull --rebase

echo "[exsync 2/4] git status"
git status -sb

echo "[exsync 3/4] python version"
python --version

echo "[exsync 4/4] tests"
PYTHONPATH="$ROOT" python -m pytest -q

echo "exsync_ok"
