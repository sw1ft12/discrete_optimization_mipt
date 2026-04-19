#!/bin/bash

TESTS=(
    "sc_157_0"
    "sc_330_0"
    "sc_1000_11"
    "sc_5000_1"
    "sc_10000_5"
    "sc_10000_2"
)

echo "Run tests..."

for test in "${TESTS[@]}"; do
    echo "Test: $test"

    cost=$(python3 $1 "data/${test}" | python3 checker.py "data/${test}")

    if [ $? -eq 0 ]; then
      echo "Test passed with total cost ${cost}"
    else
      echo "Test failed: ${cost}"
    fi

    echo
done

echo "Done"