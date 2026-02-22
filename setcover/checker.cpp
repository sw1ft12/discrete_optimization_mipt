#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <set>
#include <algorithm>

using namespace std;

struct TestCase {
    int n;
    int m;
    vector<int> costs;
    vector<vector<int>> sets;
};

struct Solution {
    vector<int> selectedSets;
    int totalCost;
};

TestCase readTest(const string& filename) {
    TestCase test;
    ifstream file(filename);

    if (!file.is_open()) {
        return test;
    }

    file >> test.n >> test.m;

    test.costs.resize(test.m);
    test.sets.resize(test.m);

    string line;
    getline(file, line);

    for(int i = 0; i < test.m; i++) {
        string line;
        getline(file, line);
        stringstream ss(line);

        ss >> test.costs[i];
        int elem;
        while(ss >> elem) {
            test.sets[i].push_back(elem);
        }
    }

    file.close();
    return test;
}


Solution readSolution() {
    Solution sol;

    string line;
    getline(cin, line);
    istringstream ss(line);
    ss >> sol.totalCost;

    while(getline(cin, line)) {
        ss = istringstream(line);
        int elem;
        while(ss >> elem) {
            sol.selectedSets.push_back(elem);
        }
    }

    return sol;
}


bool checkSolution(const TestCase& test, const Solution& sol) {
    vector<bool> covered(test.n);
    int totalCost = 0;
    for(auto setID : sol.selectedSets) {
        for(auto elem : test.sets[setID]) {
            covered[elem] = true;
        }
        totalCost += test.costs[setID];
    }

    vector<int> uncoveredElems;
    for(size_t i = 0; i < test.n; i++) {
        if(!covered[i]) {
            uncoveredElems.push_back(i);
        }
    }

    if(uncoveredElems.size() != 0) {
        cerr << "Uncovered elements:\n";
        for(auto elem : uncoveredElems) {
            cerr << elem << ' ';
        }
        cerr << '\n';
        return false;
    }

    if(totalCost != sol.totalCost) {
        cerr << "Actual cost " << totalCost << " not equals greedy cost " << sol.totalCost << '\n';
        return false;
    }

    return true;
}


int main(int argc, char* argv[]) {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    string testFile = argv[1];

    TestCase test = readTest(testFile);
    if (test.m == 0) {
        cerr << "Failed to read test " << testFile << '\n';
        return 1;
    }

    Solution sol = readSolution();

    if(!checkSolution(test, sol)) {
        return 1;
    }

    cout << sol.totalCost << '\n';
}