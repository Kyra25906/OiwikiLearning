#include <iostream>
#include <vector>
using namespace std;

struct Fenwick {
    int n;
    vector<long long> bit;
    explicit Fenwick(int length) : n(length), bit(length + 1, 0) {}
    void add(int i, long long delta) {
        for (; i <= n; i += i & -i) bit[i] += delta;
    }
    long long prefix(int i) const {
        long long result = 0;
        for (; i > 0; i -= i & -i) result += bit[i];
        return result;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    Fenwick tree(n);
    for (int i = 1; i <= n; ++i) {
        long long x;
        cin >> x;
        tree.add(i, x);
    }
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int i;
            long long delta;
            cin >> i >> delta;
            tree.add(i, delta);
        } else {
            int l, r;
            cin >> l >> r;
            cout << tree.prefix(r) - tree.prefix(l - 1) << '\n';
        }
    }
}
