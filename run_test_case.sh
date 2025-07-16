#!/bin/bash

# filepath: /home/julio/repos/ti1-2025-1-e2_vestigiosdeunaverdadsepultada/run_test.sh

# Check if a test name was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <test_name>"
  echo "Example: $0 test_diagonalish_path_in_roomA"
  exit 1
fi

# Test name provided as the first argument
TEST_NAME=$1

# Run pytest with the specified test
pytest -s tests/test_path.py::$TEST_NAME
