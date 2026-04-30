#!/bin/bash

TESTS=(
    "vrp_16_3_1"
    "vrp_26_8_1"
    "vrp_51_5_1"
    "vrp_101_10_1"
    "vrp_200_16_1"
    "vrp_421_41_1"
)

echo "Run tests..."

for test in "${TESTS[@]}"; do
    echo "Test: $test"

    start=$(date +%s)

    cost=$(python3 $1 "data/${test}" | python3 checker.py "data/${test}")
    status=$?

    end=$(date +%s)

    runtime=$(echo "$end - $start" | bc)

    echo "Time: ${runtime} seconds"

    if [ $status -eq 0 ]; then
      echo "Test passed with total cost ${cost}"
    else
      echo "Test failed: ${cost}"
    fi
done

echo "Done"