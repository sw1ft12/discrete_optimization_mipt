#!/bin/bash

TESTS=(
    "tsp_51_1"
    "tsp_100_3"
    "tsp_200_2"
    "tsp_574_1"
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