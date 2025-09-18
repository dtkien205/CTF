#!/usr/bin/env python3
import socket
import re
from time import sleep

# ----- THAY ĐỔI NẾU CẦN -----
HOST = "103.197.184.48"
PORT = 12347
P = 1_000_000_007
N = 5
# ---------------------------

# Utility matrix functions (mod P)
def modinv(a, p=P): return pow(a, p-2, p)
def mat_mul(A,B):
    r=len(A); m=len(A[0]); c=len(B[0])
    C=[[0]*c for _ in range(r)]
    for i in range(r):
        for k in range(m):
            aik=A[i][k]
            if aik==0: continue
            for j in range(c):
                C[i][j]=(C[i][j]+aik*B[k][j])%P
    return C
def mat_transpose(A): return [list(row) for row in zip(*A)]
def mat_inv(A):
    n=len(A)
    M=[ [x%P for x in row] + [1 if i==j else 0 for j in range(n)] for i,row in enumerate(A) ]
    for col in range(n):
        piv=None
        for r in range(col,n):
            if M[r][col]!=0:
                piv=r; break
        if piv is None: raise ValueError("Not invertible")
        if piv!=col: M[col], M[piv] = M[piv], M[col]
        invp = modinv(M[col][col])
        M[col] = [(v*invp) % P for v in M[col]]
        for r in range(n):
            if r==col: continue
            f = M[r][col]
            if f:
                M[r] = [ (M[r][k] - f * M[col][k]) % P for k in range(2*n) ]
    return [ row[n:] for row in M ]

def build_U():
    return [[pow(k, r, P) for r in range(N)] for k in range(1, N+1)]

def flatten_row_major(F):
    parts=[]
    for r in range(N):
        for c in range(N):
            parts.append(F[r][c] % P)
    return parts

def try_decode_parts(parts, maxCH=16):
    candidates=[]
    for CH in range(1, maxCH+1):
        allb = b''
        ok = True
        for part in parts:
            # check fit
            if part >= 1 << (8*CH):
                ok=False; break
            allb += part.to_bytes(CH, 'big')
        if not ok: continue
        cand = allb.rstrip(b'\x00')
        try:
            txt = cand.decode()
        except:
            continue
        if all(32 <= ord(ch) <= 126 for ch in txt):
            candidates.append((CH, txt))
    return candidates

# connect & query
def fetch_oracle(host,port):
    s = socket.create_connection((host,port), timeout=8)
    s_file = s.makefile('rw', buffering=1, newline='\n')
    # read initial banner lines (a few). We will read until prompt or a limited number of lines.
    banner = []
    for _ in range(10):
        try:
            line = s_file.readline()
            if not line:
                break
            banner.append(line.rstrip('\n'))
            # typical prompt might be ">> " or similar; break if seen
            if ">>" in line or "Commands" in line:
                break
        except Exception:
            break
    # now send queries row-major
    results = []
    pat = re.compile(r"= *(-?\d+)")
    for i in range(1, N+1):
        for j in range(1, N+1):
            q = f"{i} {j}\n"
            s_file.write(q)
            # read response lines until we find s_ij = number
            got = None
            for _ in range(10):
                line = s_file.readline()
                if not line:
                    break
                m = pat.search(line)
                if m:
                    got = int(m.group(1))
                    break
            if got is None:
                # try a short sleep + read more
                sleep(0.1)
                more = s_file.readline()
                m = pat.search(more or "")
                if m:
                    got = int(m.group(1))
            if got is None:
                raise SystemExit(f"Không parse được response cho {i},{j}. Vừa đọc: {line!r}")
            print(f"got s_{i}{j} = {got}")
            results.append(got)
    # close connection
    s_file.close(); s.close()
    return results

def main():
    parts = fetch_oracle(HOST, PORT)  # list length 25
    # build matrices
    A = [ parts[r*5:(r+1)*5] for r in range(5) ]
    U = build_U()
    Uinv = mat_inv(U)
    Vt = mat_transpose(U)
    Vt_inv = mat_inv(Vt)
    temp = mat_mul(Uinv, A)
    F = mat_mul(temp, Vt_inv)
    parts2 = flatten_row_major(F)
    print("\nRecovered numeric parts (25):")
    for idx, pval in enumerate(parts2):
        print(f"part[{idx}] = {pval}")
    print("\nTrying decode CH from 1..16:")
    cands = try_decode_parts(parts2, maxCH=16)
    if not cands:
        print("Không tìm candidate trong CH=1..16. Hãy tăng maxCH nếu cần.")
    else:
        for ch, s in cands:
            print(f"CH={ch} -> {s}")

if __name__ == "__main__":
    main()
