#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    long long sum = 0, mx = a[0];
    int cnt = 0;
    for (long long x : a) {
        sum += x;
        if (x > mx) {
            mx = x;
            cnt = 1;  // 新最大值取代旧最大值
        } else if (x == mx) {
            ++cnt;
        }
    }
    cout << sum << ' ' << mx << ' ' << cnt << '\n';
}
