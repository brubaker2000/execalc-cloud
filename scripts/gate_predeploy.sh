#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$(dirname "$0")/.."

echo "[gate 1/2] compile"
python3 -m compileall -q src

echo "[gate 2/2] tests"
(cd "$ROOT" && PYTHONPATH="$ROOT" python -m pytest -q)

echo "gate_ok"
