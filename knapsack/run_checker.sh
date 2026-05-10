#!/bin/bash

TESTS=(
    "ks_30_0"
    "ks_50_0"
    "ks_200_0"
    "ks_400_0"
    "ks_1000_0"
    "ks_10000_0"
)

echo "Run tests..."

for test in "${TESTS[@]}"; do
    echo "Test: $test"

    totalCost=$(python3 $1 < "data/${test}" | python3 checker.py "data/${test}" --quiet)
    if [ $? -eq 0 ]; then
      echo "Test passed with total cost ${totalCost}"
    else
      echo "Test failed: ${totalCost}"
    fi

    echo
done

echo "Done"