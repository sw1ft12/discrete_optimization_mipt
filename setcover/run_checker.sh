#!/bin/bash

g++ -std=c++17 $1 -o solution

g++ -std=c++17 checker.cpp -o checker

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

    totalCost=$(./solution < "data/${test}" | ./checker "data/${test}" --quiet)
    if [ $? -eq 0 ]; then
      echo "Test passed with total cost ${totalCost}"
    else
      echo "Test failed: ${totalCost}"
    fi

    echo
done

echo "Done"

rm checker solution