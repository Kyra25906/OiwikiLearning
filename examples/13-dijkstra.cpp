#include <functional>
#include <iostream>
#include <limits>
#include <queue>
#include <utility>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, source;
    if (!(cin >> n >> m >> source)) return 0;
    vector<vector<pair<int, long long>>> graph(n + 1);
    for (int i = 0; i < m; ++i) {
        int u, v;
        long long weight;
        cin >> u >> v >> weight;
        graph[u].push_back({v, weight});
    }
    const long long INF = numeric_limits<long long>::max() / 4;
    vector<long long> dist(n + 1, INF);
    using State = pair<long long, int>;
    priority_queue<State, vector<State>, greater<State>> heap;
    dist[source] = 0;
    heap.push({0, source});
    while (!heap.empty()) {
        auto [d, u] = heap.top();
        heap.pop();
        if (d != dist[u]) continue;  // 跳过旧记录
        for (auto [v, weight] : graph[u]) {
            if (d + weight < dist[v]) {
                dist[v] = d + weight;
                heap.push({dist[v], v});
            }
        }
    }
    for (int u = 1; u <= n; ++u) {
        if (u > 1) cout << ' ';
        cout << (dist[u] == INF ? -1 : dist[u]);
    }
    cout << '\n';
}
