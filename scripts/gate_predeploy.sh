#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[gate 1/2] compile"
python3 -m compileall -q src

echo "[gate 2/2] tests"
pytest -q

echo "gate_ok"
