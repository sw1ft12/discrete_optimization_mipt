#include <iostream>
#include <vector>

using namespace std;

struct Item {
    int cost;
    int weight;
    Item(int cost, int weight) : cost(cost), weight(weight) {}
};

int main() {
    int n, w;
    cin >> n >> w;
    vector<Item> items;
    items.reserve(n);
    for(size_t i = 0; i < n; i++) {
        int u, v;
        cin >> u >> v;
        items.emplace_back(u, v);
    }

    vector<int> dp(w+1);
    vector<int> dp_next(w+1);

    for(size_t i = 0; i < n; i++) {
        for(size_t j = 0; j <= w; j++) {
            dp_next[j] = dp[j];
            if(j >= items[i].weight) {
                dp_next[j] = max(dp_next[j], dp[j-items[i].weight] + items[i].cost);
            }
        }
        dp = dp_next;
    }

    cout << dp[w] << '\n';
}
