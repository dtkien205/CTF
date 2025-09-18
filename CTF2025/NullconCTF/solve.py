#!/usr/bin/env python3
import socket
import re

HOST = "52.59.124.14"
PORT = 5101
E = 3

def parse_banner(sock):
    f = sock.makefile("r")
    L  = int(f.readline().strip())
    n  = int(f.readline().strip())
    c1 = int(f.readline().strip(), 16)
    c2 = int(f.readline().strip(), 16)
    return L, n, c1, c2

def classify_response(resp: bytes) -> bool:
    if not resp:
        return False
    low = resp.lower()
    if b"invalid" in low or b"bad" in low or b"false" in low or b"error" in low:
        return False
    if b"valid" in low or b"ok" in low or b"correct" in low or b"true" in low:
        return True
    s = low.strip()
    if s in (b"0", b"1"):
        return s == b"1"
    # Chưa rõ → coi như False, nhưng in debug để tinh chỉnh nếu cần
    print(f"[WARN] Unrecognized oracle response, treating as invalid: {resp!r}")
    return False

def oracle(base_c, s, n, e):
    c = (base_c * pow(s, e, n)) % n
    payload = (format(c, "x") + "\n").encode()

    with socket.create_connection((HOST, PORT), timeout=6) as sock:
        f = sock.makefile("rwb", buffering=0)
        # Bỏ 4 dòng banner (server nào cũng in lại 4 dòng này)
        for _ in range(4):
            line = f.readline()
            if not line:
                break
        f.write(payload); f.flush()

        # Đọc vài dòng phản hồi (đa số 1 dòng)
        resp = b""
        for _ in range(4):
            line = f.readline()
            if not line:
                break
            resp += line
            lw = line.lower()
            if (b"valid" in lw or b"invalid" in lw or b"ok" in lw or
                b"bad" in lw or b"correct" in lw or b"false" in lw or
                lw.strip() in (b"0", b"1")):
                break

    print(f"[DEBUG oracle] s={s}, resp={resp.strip()!r}")
    return classify_response(resp)

def merge_intervals(intervals):
    if not intervals: return []
    intervals.sort()
    out = [intervals[0]]
    for a,b in intervals[1:]:
        la,lb = out[-1]
        if a <= lb + 1:
            out[-1] = (la, max(lb, b))
        else:
            out.append((a,b))
    return out

def bleichenbacher(n, e, c0, k):
    B = 1 << (8*(k-2))
    # 2.a: tìm s1 sao cho 2B <= m' < 3B
    s = (n + 3*B - 1)//(3*B)
    while True:
        if oracle(c0, s, n, e): break
        s += 1

    M = [(2*B, 3*B-1)]
    while True:
        if len(M) >= 2:
            s += 1
            while True:
                if oracle(c0, s, n, e): break
                s += 1
        else:
            a,b = M[0]
            r = (2*(b*s - 2*B) + (n-1)) // n
            found = False
            while not found:
                s_low  = (2*B + r*n + b - 1)//b
                s_high = (3*B - 1 + r*n)//a
                for s in range(s_low, s_high+1):
                    if oracle(c0, s, n, e):
                        found = True
                        break
                r += 1

        # Cập nhật M
        newM = []
        for a,b in M:
            r_low  = (a*s - 3*B + 1 + n - 1)//n
            r_high = (b*s - 2*B)//n
            for r in range(r_low, r_high+1):
                new_a = max(a, (2*B + r*n + s - 1)//s)
                new_b = min(b, (3*B - 1 + r*n)//s)
                if new_a <= new_b:
                    newM.append((new_a, new_b))
        M = merge_intervals(newM)
        print(f"[DEBUG] intervals={M}")
        if len(M) == 1 and M[0][0] == M[0][1]:
            return M[0][0]

def strip_pkcs1_v1_5(m_bytes):
    # 00 02 PS(>=8,!=00) 00 M
    if len(m_bytes) < 11 or m_bytes[0] != 0x00 or m_bytes[1] != 0x02:
        return None
    try:
        sep = m_bytes.index(0x00, 2)
    except ValueError:
        return None
    return m_bytes[sep+1:]

def fallback_scan_flag(m_bytes):
    # Khi không có 0x00 separator: tìm ENO{...}
    try:
        s = m_bytes.decode("latin-1", errors="ignore")
    except:
        return None
    m = re.search(r"ENO\{[^}\n]{0,300}\}", s)
    return m.group(0).encode() if m else None

def main():
    # Lấy 4 dòng banner ban đầu
    with socket.create_connection((HOST, PORT), timeout=6) as sock:
        L, n, c1, c2 = parse_banner(sock)

    k = (n.bit_length() + 7)//8
    print(f"[+] len(flag)={L}, k={k}, n bits={n.bit_length()}")
    print("[+] Attack starting...")

    # Bạn có thể dùng c1 hoặc c2, cả hai cùng plaintext
    m = bleichenbacher(n, E, c1, k)
    mb = m.to_bytes(k, "big")

    msg = strip_pkcs1_v1_5(mb)
    if msg is not None:
        try:
            print("[+] Flag:", msg.decode())
        except:
            print("[+] Plaintext (hex):", msg.hex())
        return

    print("[-] No 0x00 separator found. Raw block (hex):", mb.hex())
    alt = fallback_scan_flag(mb)
    if alt:
        try:
            print("[+] Flag (fallback scan):", alt.decode())
        except:
            print("[+] Flag (fallback scan, hex):", alt.hex())
    else:
        print("[-] Fallback scan failed. Share a few [DEBUG oracle] lines to refine detection.")

if __name__ == "__main__":
    main()
