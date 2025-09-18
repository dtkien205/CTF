#!/usr/bin/env python3
# Solve repeating-key XOR where the key is built from the plaintext's
# contiguous hex runs (pair digits -> 1 byte, leftover single nibble -> 0x0n).

import string
from itertools import product

# ==== DÁN CIPHERTEXT Ở ĐÂY (từ ảnh bạn gửi) ====
cipher_hex = """
65 6c ce 6b c1 75 61 7e 53 66 c9 52 d8 6c 6a
53 6e 6e de 52 df 63 6d 7e 75 7f ce 64 d5 63 73
""".strip()
# ===============================================

C = bytes.fromhex(cipher_hex.replace("\n", " ").replace("\t", " ").strip())
n = len(C)

ALLOWED = (string.ascii_lowercase + string.digits + "_{}").encode()

def key_from_plain_hex_runs(plain_bytes: bytes) -> bytes:
    """Lấy key theo quy tắc CyberChef HEX trong ảnh:
       - Duyệt trái→phải, gom các ký tự hex liên tiếp (0-9 a-f).
       - Mỗi cặp nibble -> 1 byte (hi<<4 | lo).
       - Nếu lẻ, nibble cuối -> 1 byte 0x0n.
    """
    hexd = set(b"0123456789abcdef")
    out = []
    i = 0
    while i < len(plain_bytes):
        if plain_bytes[i] in hexd:
            j = i
            while j < len(plain_bytes) and plain_bytes[j] in hexd:
                j += 1
            run = plain_bytes[i:j]
            k = 0
            while k + 1 < len(run):
                out.append((int(chr(run[k]), 16) << 4) | int(chr(run[k+1]), 16))
                k += 2
            if k < len(run):  # nibble lẻ
                out.append(int(chr(run[k]), 16))
            i = j
        else:
            i += 1
    return bytes(out)

def solve():
    # Thử độ dài key m nhỏ (thực tế m rất nhỏ do chỉ tính trên chữ cái hex)
    for m in range(1, 20):
        # Xác lập tập giá trị khả dĩ cho từng K[r]
        poss = [set(range(256)) for _ in range(m)]

        # Ép prefix/suffix theo format flag
        known = {0: b"i", 1: b"c", 2: b"t", 3: b"f", 4: b"{", n - 1: b"}"}
        ok = True
        for i, ch in known.items():
            r = i % m
            k = C[i] ^ ch[0]
            poss[r] &= {k}
            if not poss[r]:
                ok = False
                break
        if not ok:
            continue

        # Với các vị trí khác, giới hạn sao cho plaintext thuộc ALLOWED
        allowed_set = set(ALLOWED)
        for i in range(n):
            if i in known:
                continue
            r = i % m
            poss[r] &= {C[i] ^ p for p in allowed_set}
            if not poss[r]:
                ok = False
                break
        if not ok:
            continue

        # Nếu không quá nhiều tổ hợp, duyệt hết và kiểm tra quy tắc tạo key
        total = 1
        for s in poss:
            total *= len(s)
            if total > 100000:  # cắt tỉa
                ok = False
                break
        if not ok:
            continue

        for choice in product(*[sorted(s) for s in poss]):
            K = bytes(choice)
            P = bytes(C[i] ^ K[i % m] for i in range(n))
            if not (P.startswith(b"ictf{") and P.endswith(b"}") and all(c in ALLOWED for c in P)):
                continue
            # Kiểm tra key dựng lại từ plaintext có đúng K không
            if key_from_plain_hex_runs(P) == K:
                return m, K, P

    return None, None, None

if __name__ == "__main__":
    m, K, P = solve()
    if P:
        print("m =", m)
        print("Key (hex) =", K.hex())
        print("Flag =", P.decode())
    else:
        print("Không tìm được lời giải. Kiểm tra lại ciphertext hoặc quy tắc key.")
