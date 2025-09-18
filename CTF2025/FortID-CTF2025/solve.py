#!/usr/bin/env python3
import sys, re, socket

HOST = "0.cloud.chals.io"
PORT = 32957

DOMAIN = list(range(0, 2049))         # secret ∈ [0..2048]
C = 0xD3ADC0DE                        # constant in server

def recvline(sock, timeout=5):
    sock.settimeout(timeout)
    data = b""
    while True:
        ch = sock.recv(1)
        if not ch:
            break
        data += ch
        if ch == b'\n':
            break
    return data.decode(errors="ignore") if data else None

def sendline(sock, s):
    sock.sendall((s + "\n").encode())

def t_mod_for_guess(n, s_guess):
    return (-C - s_guess) % n

def x_from_t(n, t_mod):
    return 1 + n * t_mod

def build_half_for_bit(n, bit_index, target_len, used_x):
    batch = []
    subset = [s for s in DOMAIN if ((s >> bit_index) & 1) == 1]
    for s in subset:
        t = t_mod_for_guess(n, s)
        x = x_from_t(n, t)
        if x in used_x:
            x = x + n * n
        used_x.add(x)
        batch.append(x)

    dummy_s = 3000000000 + (bit_index * 1000000)
    while len(batch) < target_len:
        t = t_mod_for_guess(n, dummy_s)
        x = x_from_t(n, t)
        if x in used_x:
            dummy_s += 1
            continue
        used_x.add(x)
        batch.append(x)
        dummy_s += 1

    return batch

def solve_round(sock):
    # Read until we get 'n = ...'
    while True:
        line = recvline(sock)
        if line is None:
            return False
        if "n =" in line:
            break
    m = re.search(r"n = (\\d+)", line)
    if not m:
        # maybe next line
        line2 = recvline(sock)
        if not line2:
            return False
        m = re.search(r"n = (\\d+)", line2)
        if not m:
            return False
    n = int(m.group(1))

    # "You can ask 7 questions:"
    _ = recvline(sock)

    queries = []
    bit_pairs = [(0,1), (2,3), (4,5), (6,7), (8,9), (10, -1), (-1, -1)]

    for (bL, bR) in bit_pairs:
        used_x = set()
        left_size = 0 if bL < 0 else sum(((s >> bL) & 1) == 1 for s in DOMAIN)
        right_size = 0 if bR < 0 else sum(((s >> bR) & 1) == 1 for s in DOMAIN)
        target = max(left_size, right_size)

        if bL >= 0:
            left = build_half_for_bit(n, bL, target, used_x)
        else:
            left = []
        if bR >= 0:
            right = build_half_for_bit(n, bR, target, used_x)
        else:
            right = []

        total_len = len(left) + len(right)
        if total_len % 2 == 1:
            dummy_s = 4000000000 + len(queries)
            while True:
                t = t_mod_for_guess(n, dummy_s)
                x = x_from_t(n, t)
                if x not in used_x:
                    used_x.add(x)
                    right.append(x)
                    break
                dummy_s += 1

        q = left + right
        queries.append(q)

    # Send queries
    for q in queries:
        sendline(sock, " ".join(str(x) for x in q))

    # Read 7 lines of outputs "L R"
    bits = [0]*11
    for (bL, bR) in bit_pairs:
        line = recvline(sock)
        if line is None:
            return False
        parts = line.strip().split()
        if len(parts) != 2:
            return False
        L = int(parts[0])
        R = int(parts[1])
        if bL >= 0 and L == 0:
            bits[bL] = 1
        if bR >= 0 and R == 0:
            bits[bR] = 1

    # "Can you guess my secret?"
    _ = recvline(sock)

    secret = 0
    for k in range(11):
        if bits[k]:
            secret |= (1 << k)

    sendline(sock, str(secret))

    verdict = recvline(sock)
    if verdict is None or "Correct!" not in verdict:
        sys.stderr.write("[!] Wrong guess or protocol mismatch: %r\\n" % (verdict,))
        return False
    return True

def main():
    sock = socket.create_connection((HOST, PORT))
    for _ in range(10):
        if not solve_round(sock):
            return
    # Read flag line
    line = recvline(sock)
    if line and "Here you go:" in line:
        print(line.strip())
    else:
        # Try read more
        sock.settimeout(2)
        try:
            rest = sock.recv(4096).decode(errors="ignore")
            if rest:
                print(rest.strip())
        except:
            pass

if __name__ == "__main__":
    main()
