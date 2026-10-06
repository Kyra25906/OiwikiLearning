#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, q;
    if (!(cin >> n >> m >> q)) return 0;
    vector<long long> diff(n + 2, 0), prefix(n + 1, 0);
    long long previous = 0;
    for (int i = 1; i <= n; ++i) {
        long long x;
        cin >> x;
        diff[i] = x - previous;
        previous = x;
    }
    for (int i = 0; i < m; ++i) {
        int l, r;
        long long v;
        cin >> l >> r >> v;
        diff[l] += v;
        diff[r + 1] -= v;
    }
    long long current = 0;
    for (int i = 1; i <= n; ++i) {
        current += diff[i];
        prefix[i] = prefix[i - 1] + current;
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << prefix[r] - prefix[l - 1] << '\n';
    }
}
