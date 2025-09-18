#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, binascii
from pathlib import Path

# ---- utils ----
def hex_to_int(hexs): return int.from_bytes(binascii.unhexlify(hexs.strip()), 'big')
def hex_to_bytes(hexs): return binascii.unhexlify(hexs.strip())

def bytes_to_bits_msb(b):
    out = []
    for by in b:
        for k in range(7, -1, -1):
            out.append((by >> k) & 1)
    return out

def bits_to_bytes_msb(bits):
    n = len(bits)
    m = (n + 7)//8
    val = 0
    for b in bits:
        val = (val << 1) | (b & 1)
    return val.to_bytes(m, 'big')

def row_first_nbits(row_hex, nbits, total_bits=504):
    """row_hex là 63 byte (504 bit). Lấy nbits MSB."""
    v = hex_to_int(row_hex)
    shift = total_bits - nbits
    return (v >> shift) & ((1 << nbits) - 1)

# ---- Gauss-Jordan RREF trên GF(2) ----
def solve_gf2(A_rows, b_bits, ncols):
    """
    A_rows: list[int], mỗi int là 1 hàng (nbits = ncols),
    b_bits: list[int] độ dài = số hàng,
    ncols: số cột (497)
    Trả về: list[int] Z_bits độ dài ncols (free var = 0)
    """
    m = len(A_rows)
    aug = [(A_rows[r] << 1) | (b_bits[r] & 1) for r in range(m)]
    row = 0
    for col in range(ncols):
        mask = 1 << (ncols - col)
        piv = None
        for r in range(row, m):
            if aug[r] & mask:
                piv = r; break
        if piv is None:
            continue
        if piv != row:
            aug[row], aug[piv] = aug[piv], aug[row]
        for r in range(m):
            if r != row and (aug[r] & mask):
                aug[r] ^= aug[row]
        row += 1
        if row == m: break

    # check consistency
    for r in range(row, m):
        if (aug[r] & ((1 << (ncols+1)) - 2)) == 0 and (aug[r] & 1):
            raise RuntimeError("Inconsistent system")

    # extract 1 nghiệm (free vars = 0)
    Z_bits = [0]*ncols
    ridx = 0
    for col in range(ncols):
        mask = 1 << (ncols - col)
        if ridx < m and (aug[ridx] & mask):
            Z_bits[col] = aug[ridx] & 1
            ridx += 1
        else:
            Z_bits[col] = 0
    return Z_bits, row

# ---- parse public.txt ----
def parse_public(path):
    lines = Path(path).read_text(encoding='utf-8', errors='replace').splitlines()
    assert lines[0].startswith("N=")
    assert lines[1].startswith("D=")
    N = int(lines[0].split("=")[1])
    D = int(lines[1].split("=")[1])

    i = 0
    samples = []
    while i < len(lines):
        if lines[i] == "BEGIN SAMPLE":
            i += 1
            m = int(lines[i].split("=")[1]); i += 1
            assert lines[i] == "L:"; i += 1
            L = lines[i:i+m]; i += m
            assert lines[i].startswith("P=")
            P_hex = lines[i].split("=",1)[1]; i += 1
            assert lines[i].startswith("C=")
            C_hex = lines[i].split("=",1)[1]; i += 1
            assert lines[i] == "END SAMPLE"; i += 1
            samples.append((m, L, P_hex, C_hex))
        elif lines[i] == "BEGIN FLAG":
            i += 1
            mF = int(lines[i].split("=")[1]); i += 1
            assert lines[i] == "L:"; i += 1
            LF = lines[i:i+mF]; i += mF
            assert lines[i].startswith("C=")
            CF_hex = lines[i].split("=",1)[1]; i += 1
            assert lines[i] == "END FLAG"; i += 1
            flag_block = (mF, LF, CF_hex)
        else:
            i += 1
    return N, D, samples, flag_block

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 solve_public.py public.txt")
        sys.exit(1)

    N, D, samples, flag_block = parse_public(sys.argv[1])
    assert D == 497, "D phải là 497 (1 + N + C(N,2))"

    # Xây hệ phương trình cho Z theo mô hình: (P XOR C) = L_first497 * Z
    A_rows = []
    b_bits = []
    for (m, L, P_hex, C_hex) in samples:
        P_b = hex_to_bytes(P_hex)
        C_b = hex_to_bytes(C_hex)
        assert len(P_b) == len(C_b) == (m + 7)//8
        rhs_bits = bytes_to_bits_msb(bytes(x ^ y for x,y in zip(P_b, C_b)))[:m]
        for r in range(m):
            A_rows.append(row_first_nbits(L[r], 497))   # dùng 497 bit MSB
            b_bits.append(rhs_bits[r])

    Z_bits, rank = solve_gf2(A_rows, b_bits, 497)
    # print(f"[+] rank={rank}/497")

    # Giải FLAG: P_flag = C_flag XOR (L_flag_first497 * Z)
    mF, LF, CF_hex = flag_block
    Z_int = int(''.join(str(b) for b in Z_bits), 2)

    # y = L * Z
    y_bits = []
    for r in range(mF):
        row = row_first_nbits(LF[r], 497)
        y_bits.append((row & Z_int).bit_count() & 1)
    y_bytes = bits_to_bytes_msb(y_bits)

    C_flag = hex_to_bytes(CF_hex)
    P_flag = bytes(c ^ y for c,y in zip(C_flag, y_bytes))

    # In flag
    try:
        print(P_flag.decode('utf-8'))
    except UnicodeDecodeError:
        print(P_flag)

if __name__ == "__main__":
    main()
