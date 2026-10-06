#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<vector<int>> graph(n + 1);
    vector<int> indegree(n + 1, 0);
    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        ++indegree[v];
    }
    queue<int> ready;
    for (int u = 1; u <= n; ++u) {
        if (indegree[u] == 0) ready.push(u);
    }
    vector<int> order;
    while (!ready.empty()) {
        int u = ready.front();
        ready.pop();
        order.push_back(u);
        for (int v : graph[u]) {
            if (--indegree[v] == 0) ready.push(v);
        }
    }
    if (static_cast<int>(order.size()) != n) cout << "IMPOSSIBLE\n";
    else {
        for (int i = 0; i < n; ++i) {
            if (i) cout << ' ';
            cout << order[i];
        }
        cout << '\n';
    }
}
