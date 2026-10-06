#include <iostream>
#include <queue>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int h, w;
    if (!(cin >> h >> w)) return 0;
    vector<string> grid(h);
    for (auto &row : grid) cin >> row;
    if (grid[0][0] == '#' || grid[h - 1][w - 1] == '#') {
        cout << -1 << '\n';
        return 0;
    }
    vector<vector<int>> dist(h, vector<int>(w, -1));
    queue<pair<int, int>> q;
    dist[0][0] = 0;
    q.push({0, 0});
    const int dr[4] = {-1, 0, 1, 0};
    const int dc[4] = {0, 1, 0, -1};
    while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        for (int k = 0; k < 4; ++k) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= h || nc < 0 || nc >= w) continue;
            if (grid[nr][nc] == '#' || dist[nr][nc] != -1) continue;
            dist[nr][nc] = dist[r][c] + 1;
            q.push({nr, nc});
        }
    }
    cout << dist[h - 1][w - 1] << '\n';
}
