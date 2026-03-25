#!/bin/bash

TESTS=(
    "gc_50_3"
    "gc_70_7"
    "gc_100_5"
    "gc_250_9"
    "gc_500_1"
    "gc_1000_5"
)

echo "Run tests..."

for test in "${TESTS[@]}"; do
    echo "Test: $test"

    totalColors=$(python3 $1 < "data/${test}" | python3 checker.py "data/${test}")
    if [ $? -eq 0 ]; then
      echo "Test passed with total colors ${totalColors}"
    else
      echo "Test failed: ${totalColors}"
    fi

    echo
done

echo "Done"