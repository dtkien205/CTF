# try_fix_top_bits.py
from math import gcd

# giá trị bạn đã thu được
p_recovered = 0x17f865abe9fc4a5446a06208b7a0073a333a22a25e2e95684b0b27a375bc47df

N = int("7fed997cfb3a3e8440142aba39d2c62ef03e773f8d98d7d373b3e8336903ca122cdffa11fd4de735776c9aefdd1607c70f0c403bd745d2e3065fede7f22dbfa94ea22b833b2442bd474a88694305b0f389162ca25eddf2673baeb3b6a2855842a0a0a022a2a222a28802a2022888822a8a20aa20a28022a08088200a8a800801", 16)
C = int("16c88a06c4203b9ce6f5f652a52f449ce37347afb5cb25b0a1bf0b105f158246bd64adb2b6f2a563fa747d31b9ba4af54efd9449f6b75b1ea83015fefb1e1d206f20ca31fdf47ee45bbb382c9aa6e7ff7946f9973a2edebdb412bdc48e9a157cb36eb2e599c9c0a27153983d316b0d9ce08ef9d06f536b2ff29cf5393fba056d", 16)
E = 1234567891

nbit = 256
B = 1 << nbit

def magicc(n: int) -> int:
    B = bin(n)[2:]
    M = ''.join('01' if b == '0' else '11' for b in B)
    return int(M, 2)

# Try varying top k bits of p (k = 8..16)
def try_top_bits(p_base, k_bits):
    # mask_low keeps the lowest (256 - k_bits) bits from recovered p
    low_mask = (1 << (256 - k_bits)) - 1
    low_part = p_base & low_mask
    print(f"[i] trying k_bits={k_bits}, low_part bits={(256-k_bits)}")
    limit = 1 << k_bits
    for top in range(limit):
        p_cand = low_part | (top << (256 - k_bits))
        # Ensure p_cand has correct bit-length (prime from getPrime likely has MSB=1)
        # if you want, force MSB=1 by setting top bit:
        # p_cand |= (1 << 255)
        R = magicc(p_cand)
        g = gcd(N, R)
        if 1 < g < N:
            Q = N // g
            if Q * g == N:
                print("[+] Found factors!")
                return p_cand, Q, g
    return None, None, None

# Try increasing k
for k in range(8, 17):  # 8..16 bits (256 -> 65536 tries)
    p_cand, Q, R = try_top_bits(p_recovered, k)
    if p_cand:
        print(f"[+] success with k={k}")
        break
else:
    print("[-] not found for 8..16 top bits. Consider increasing to 20 bits (1M tries),\n    or try toggling setting MSB=1 explicitly and re-run.")

if p_cand:
    # compute RSA private and message
    from math import gcd
    def egcd(a,b):
        if b==0: return (1,0,a)
        x,y,g = egcd(b, a % b)
        return (y, x - (a//b)*y, g)
    def modinv(a,m):
        x,y,g = egcd(a,m)
        if g != 1:
            raise Exception("no inv")
        return x % m

    phi = (Q - 1) * (R - 1)
    d = modinv(E, phi)
    m = pow(C, d, N)
    m_bytes = m.to_bytes((m.bit_length()+7)//8, "big")
    try:
        s = m_bytes.decode()
    except:
        s = m_bytes.decode("latin-1", errors="ignore")
    print("\n[+] INPUT STRING (paste to program to get FLAG):\n")
    print(s)
    print("\n[+] p_candidate = 0x%x\n[+] Q=0x%x\n[+] R=0x%x" % (p_cand, Q, R))
