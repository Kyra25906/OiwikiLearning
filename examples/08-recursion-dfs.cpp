#include <iostream>
#include <vector>
using namespace std;
vector<long long> a;
vector<int> chosen;
int n;
long long target, answer = 0;

void dfs(int pos, long long sum) {
    if (pos == n) {
        if (sum == target) ++answer;
        return;
    }
    dfs(pos + 1, sum);  // 不选当前位置
    chosen.push_back(pos);
    dfs(pos + 1, sum + a[pos]);
    chosen.pop_back();  // 共享路径必须恢复
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    if (!(cin >> n >> target)) return 0;
    a.resize(n);
    for (auto &x : a) cin >> x;
    dfs(0, 0);
    cout << answer << '\n';
}
