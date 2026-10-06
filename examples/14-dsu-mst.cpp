#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

struct DSU {
    vector<int> parent, size;
    explicit DSU(int n) : parent(n + 1), size(n + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        while (x != parent[x]) {
            parent[x] = parent[parent[x]];  // 路径减半
            x = parent[x];
        }
        return x;
    }
    bool merge(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (size[a] < size[b]) swap(a, b);
        parent[b] = a;
        size[a] += size[b];
        return true;
    }
};
struct Edge { int u, v; long long weight; };

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<Edge> edges(m);
    for (auto &e : edges) cin >> e.u >> e.v >> e.weight;
    sort(edges.begin(), edges.end(), [](const Edge &a, const Edge &b) {
        return a.weight < b.weight;
    });
    DSU dsu(n);
    int used = 0;
    long long total = 0;
    for (const auto &e : edges) {
        if (dsu.merge(e.u, e.v)) {
            total += e.weight;
            ++used;
            if (used == n - 1) break;
        }
    }
    if (used == n - 1) cout << total << '\n';
    else cout << "IMPOSSIBLE\n";
}
