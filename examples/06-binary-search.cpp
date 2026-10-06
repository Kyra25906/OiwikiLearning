#include <iostream>
#include <vector>
using namespace std;

int first_at_least(const vector<long long> &a, long long x) {
    int l = 0, r = static_cast<int>(a.size());
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (a[mid] >= x) r = mid;
        else l = mid + 1;
    }
    return l;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if (!(cin >> n >> q)) return 0;
    vector<long long> a(n);
    for (auto &v : a) cin >> v;
    while (q--) {
        long long x;
        cin >> x;
        cout << first_at_least(a, x) << '\n';
    }
}
