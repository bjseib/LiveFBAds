#!/usr/bin/env bash
set -euo pipefail

if [[ -d .venv ]]; then
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

pip install -r requirements.txt
python -m pytest "$@"
