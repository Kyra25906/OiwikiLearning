#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, capacity;
    if (!(cin >> n >> capacity)) return 0;
    vector<long long> dp(capacity + 1, 0);
    for (int i = 0; i < n; ++i) {
        int weight;
        long long value;
        cin >> weight >> value;
        for (int c = capacity; c >= weight; --c) {
            dp[c] = max(dp[c], dp[c - weight] + value);
        }
    }
    cout << dp[capacity] << '\n';
}
