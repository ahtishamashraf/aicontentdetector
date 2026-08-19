#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e './backend[dev]'
npm --prefix frontend ci
