#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<long long> cost(n);
    for (auto &x : cost) cin >> x;
    sort(cost.begin(), cost.end());
    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; ++i) prefix[i + 1] = prefix[i] + cost[i];
    while (q--) {
        long long budget;
        cin >> budget;
        auto it = upper_bound(prefix.begin(), prefix.end(), budget);
        int answer = static_cast<int>(it - prefix.begin()) - 1;
        cout << answer << '\n';
    }
}
