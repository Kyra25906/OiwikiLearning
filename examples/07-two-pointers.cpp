#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long target;
    if (!(cin >> n >> target)) return 0;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    int l = 0, r = n - 1;
    long long ans = 0;
    while (l < r) {
        long long sum = a[l] + a[r];
        if (sum < target) ++l;
        else if (sum > target) --r;
        else if (a[l] == a[r]) {
            long long count = r - l + 1;
            ans += count * (count - 1) / 2;
            break;
        } else {
            long long left_value = a[l], right_value = a[r];
            long long left_count = 0, right_count = 0;
            while (l <= r && a[l] == left_value) {
                ++l;
                ++left_count;
            }
            while (l <= r && a[r] == right_value) {
                --r;
                ++right_count;
            }
            ans += left_count * right_count;
        }
    }
    cout << ans << '\n';
}
