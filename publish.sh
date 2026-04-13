#!/usr/bin/env bash
# publish.sh — publish utract-mcp to PyPI or TestPyPI
# Usage:
#   TWINE_PASSWORD=pypi-TOKEN ./publish.sh           # publishes to TestPyPI
#   TWINE_PASSWORD=pypi-TOKEN REPO=pypi ./publish.sh  # publishes to real PyPI
set -euo pipefail

REPO="${REPO:-testpypi}"
echo "Publishing to $REPO ..."
TWINE_USERNAME=__token__ python -m twine upload --repository "$REPO" dist/*
echo "Done. View at https://test.pypi.org/project/utract-mcp/ (TestPyPI)"
echo "         or https://pypi.org/project/utract-mcp/ (PyPI)"
