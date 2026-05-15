#!/bin/bash

TESTS=(
    "tsp_51_1"
    "tsp_100_3"
    "tsp_200_2"
    "tsp_574_1"
    "tsp_1889_1"
    "tsp_33810_1"
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

    echo
done

echo "Done"