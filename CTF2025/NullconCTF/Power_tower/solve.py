# -*- coding: utf-8 -*-
# Giải mã cho đoạn code sinh khóa "lũy thừa lồng nhau" (tetration) mod n
# Cần: pip install pycryptodome

from Crypto.Cipher import AES
import math, random

# ========= NHẬP DỮ LIỆU =========
n = 107502945843251244337535082460697583639357473016005252008262865481138355040617
# DÁN ciphertext hex bạn có vào đây:
cipher_hex = "b6c4d050dd08fd8471ef06e73d39b359e3fc370ca78a3426f01540985b88ba66ec9521e9b68821fed1fa625e11315bf9"
# =================================

# Danh sách số nguyên tố < 100 (đúng như code gốc)
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]

# ---- Primality test (Miller–Rabin, đủ dùng ở đây) ----
def is_probable_prime(x: int) -> bool:
    if x < 2:
        return False
    small = [2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small:
        if x % p == 0:
            return x == p
    d = x - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in small:
        if a >= x:
            continue
        v = pow(a, d, x)
        if v == 1 or v == x - 1:
            continue
        for _ in range(s - 1):
            v = (v * v) % x
            if v == x - 1:
                break
        else:
            return False
    return True

# ---- Pollard Rho + phân tích thừa số ----
def pollards_rho(x: int) -> int:
    if x % 2 == 0:
        return 2
    if x % 3 == 0:
        return 3
    while True:
        c = random.randrange(1, x - 1)
        f = lambda t: (t * t + c) % x
        a = random.randrange(0, x)
        b = a
        g = 1
        while g == 1:
            a = f(a)
            b = f(f(b))
            g = math.gcd(abs(a - b), x)
        if g != x:
            return g

def factorize(x: int, time_limit_sec: float = 20.0):
    """
    Phân tích x thành thừa số nguyên tố (khá nhanh với size như đề).
    Trả về list các thừa số (có lặp).
    """
    import time
    t0 = time.time()
    stk = [x]
    res = []
    while stk:
        m = stk.pop()
        if m == 1:
            continue
        if is_probable_prime(m):
            res.append(m)
            continue
        if time.time() - t0 > time_limit_sec:
            # nếu quá lâu thì vẫn cố rho tiếp (thường không cần nhánh này)
            d = pollards_rho(m)
            stk.append(d); stk.append(m // d)
            continue
        d = pollards_rho(m)
        stk.append(d); stk.append(m // d)
    return res

# ---- Hàm Carmichael λ(n) từ phân tích thừa số ----
def carmichael_lambda_from_factors(factors):
    # factors: list các prime (có lặp)
    from collections import Counter
    cnt = Counter(factors)
    l = 1
    for p, a in cnt.items():
        if p == 2:
            if a == 1:
                lam = 1
            elif a == 2:
                lam = 2
            else:
                lam = 2 ** (a - 2)
        else:
            lam = (p - 1) * (p ** (a - 1))
        l = l * lam // math.gcd(l, lam)
    return l

_lam_cache = {}
def lam(x: int) -> int:
    if x in _lam_cache:
        return _lam_cache[x]
    fs = factorize(x)
    L = carmichael_lambda_from_factors(fs)
    _lam_cache[x] = L
    return L

# ---- Tính “tháp lũy thừa” mod m cho danh sách primes (đúng như int_key % n) ----
def tower_mod(prs, m: int) -> int:
    """
    Kết quả bằng p_k ^ ( p_{k-1} ^ ( ... (2^1) ... ) ) mod m
    Dùng λ(m) đệ quy để rút gọn số mũ (Euler/Carmichael), cộng thêm λ(m) để đảm bảo "độ cao" lớn.
    """
    p = prs[-1]
    if len(prs) == 1:
        return pow(p, 1, m)
    lam_m = lam(m)
    e = tower_mod(prs[:-1], lam_m)
    # gcd(p, m) == 1 trong bài này (n không chia hết cho prime < 100), nên thêm lam_m là hợp lệ
    if math.gcd(p, m) == 1:
        e += lam_m
    return pow(p, e, m)

# ---- Tính khóa, giải mã ----
key_int = tower_mod(primes, n)
key_bytes = key_int.to_bytes(32, "big")  # đúng 32 byte cho AES-256
ct = bytes.fromhex(cipher_hex)
pt = AES.new(key_bytes, AES.MODE_ECB).decrypt(ct)

# Padding dùng '_' nên bỏ đuôi '_'
plain = pt.decode(errors="ignore").rstrip('_')
print(plain)
