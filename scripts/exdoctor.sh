#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[exdoctor] location: $ROOT"

echo "[exdoctor] python:"
python3 --version || true

echo "[exdoctor] git:"
git --version || true

echo "[exdoctor] gcloud:"
if command -v gcloud >/dev/null 2>&1; then
  echo "gcloud_ok"
else
  echo "gcloud_missing_or_not_in_path"
fi

echo "[exdoctor] venv:"
if [[ -f ".venv/bin/activate" ]]; then
  echo "venv_ok"
else
  echo "venv_missing"
fi

echo "[exdoctor] pytest:"
if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
  python -m pytest --version || echo "pytest_missing_in_venv"
else
  echo "skip_pytest_check_no_venv"
fi

echo "exdoctor_ok"
