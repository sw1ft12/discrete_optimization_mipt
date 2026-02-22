#include <iostream>
#include <vector>
#include <set>
#include <sstream>

using namespace std;

struct Set {
    int cost;
    vector<int> elements;
};

set<int> greedySetCover(int n, const vector<Set>& sets) {
    int m = sets.size();

    set<int> uncovered;
    for (int i = 0; i < n; i++) {
        uncovered.insert(i);
    }

    set<int> chosenSets;

    vector<bool> covered(n);

    while (!uncovered.empty()) {
        int bestSet;
        int bestSetCost = 1;
        int newElementsCovered = 0;

        for(int i = 0; i < m; i++) {
            if(chosenSets.find(i) != chosenSets.end()) {
                continue;
            }

            int newElements = 0;
            for(int elem : sets[i].elements) {
                if(!covered[elem]) {
                    newElements++;
                }
            }

            if(sets[i].cost * newElementsCovered < bestSetCost * newElements) {
                newElementsCovered = newElements;
                bestSetCost = sets[i].cost;
                bestSet = i;
            }
        }

        chosenSets.insert(bestSet);

        for(int elem : sets[bestSet].elements) {
            if(!covered[elem]) {
                covered[elem] = true;
                uncovered.erase(elem);
            }
        }
    }

    return chosenSets;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n, m;
    cin >> n >> m;
    string line;
    getline(cin, line);

    vector<Set> sets(m);

    for(int i = 0; i < m; i++) {
        getline(cin, line);
        istringstream ss(line);
        ss >> sets[i].cost;

        int elem;
        while(ss >> elem) {
            sets[i].elements.push_back(elem);
        }
    }

    set<int> chosenSets = greedySetCover(n, sets);
    int totalCost = 0;
    for(auto i : chosenSets) {
        totalCost += sets[i].cost;
    }

    cout << totalCost << '\n';

    for(auto x : chosenSets) {
        cout << x << ' ';
    }

    cout << '\n';
}