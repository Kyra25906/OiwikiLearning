#include <iostream>
using namespace std;

long long gcd_value(long long a, long long b) {
    while (b != 0) {
        long long remainder = a % b;
        a = b;
        b = remainder;
    }
    return a;
}

long long power_mod(long long base, long long exponent, long long modulus) {
    long long result = 1 % modulus;
    base %= modulus;
    while (exponent > 0) {
        if (exponent & 1LL) result = result * base % modulus;
        base = base * base % modulus;
        exponent >>= 1;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long a, b, p;
    if (!(cin >> a >> b >> p)) return 0;
    cout << gcd_value(a, b) << '\n';
    cout << power_mod(a, b, p) << '\n';
}
