#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
struct Event { long long l, r; };

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<Event> events(n);
    for (auto &e : events) cin >> e.l >> e.r;
    sort(events.begin(), events.end(), [](const Event &a, const Event &b) {
        if (a.r != b.r) return a.r < b.r;
        return a.l < b.l;
    });
    bool has = false;
    long long last = 0;
    int ans = 0;
    for (const auto &e : events) {
        if (!has || e.l >= last) {
            has = true;
            last = e.r;
            ++ans;
        }
    }
    cout << ans << '\n';
}
