#!/bin/bash

TESTS=(
    "fl_25_2"
    "fl_100_1"
    "fl_200_7"
    "fl_500_7"
    "fl_1000_2"
    "fl_2000_2"
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