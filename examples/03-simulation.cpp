#include <iostream>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string commands;
    if (!(cin >> commands)) return 0;
    const int dx[4] = {0, 1, 0, -1};
    const int dy[4] = {1, 0, -1, 0};
    const string names = "NESW";
    int x = 0, y = 0, dir = 0;
    for (char c : commands) {
        if (c == 'L') dir = (dir + 3) % 4;
        else if (c == 'R') dir = (dir + 1) % 4;
        else {
            x += dx[dir];
            y += dy[dir];
        }
    }
    cout << x << ' ' << y << ' ' << names[dir] << '\n';
}
