from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes

def egcd(a, b):
    if a == 0: return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1: raise Exception("no inverse")
    return x % m

def crt(c, n):
    x, N = 0, 1
    for ni in n: N *= ni
    for i in range(len(c)):
        Mi = N // n[i]
        ti = modinv(Mi, n[i])
        x = (x + c[i] * Mi * ti) % N
    return x, N

def nth_root(x, e):
    lo, hi = 1, x
    while lo < hi:
        mid = (lo + hi) // 2
        if pow(mid, e) < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

# Загрузка ключей и шифротекстов
n_list, c_list = [], []
for i in range(1, 6):
    with open(f"{i}.pub.pem") as f:
        key = RSA.import_key(f.read())
        n_list.append(key.n)
        e = key.e   # предполагаем, что все e одинаковы
    with open(f"{i}.enc", "rb") as f:
        c_list.append(int.from_bytes(f.read(), 'big'))

# CRT и корень
x, _ = crt(c_list[:e], n_list[:e])
m = nth_root(x, e)
flag = long_to_bytes(m).decode()
print(flag)
