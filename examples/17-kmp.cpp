#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string text, pattern;
    if (!(cin >> text >> pattern)) return 0;
    int n = static_cast<int>(text.size());
    int m = static_cast<int>(pattern.size());
    vector<int> pi(m, 0);
    for (int i = 1; i < m; ++i) {
        int j = pi[i - 1];
        while (j > 0 && pattern[i] != pattern[j]) j = pi[j - 1];
        if (pattern[i] == pattern[j]) ++j;
        pi[i] = j;
    }
    vector<int> positions;
    int j = 0;
    for (int i = 0; i < n; ++i) {
        while (j > 0 && text[i] != pattern[j]) j = pi[j - 1];
        if (text[i] == pattern[j]) ++j;
        if (j == m) {
            positions.push_back(i - m + 1);
            j = pi[j - 1];  // 保留重叠部分
        }
    }
    if (positions.empty()) cout << -1;
    else {
        for (int i = 0; i < static_cast<int>(positions.size()); ++i) {
            if (i) cout << ' ';
            cout << positions[i];
        }
    }
    cout << '\n';
}
