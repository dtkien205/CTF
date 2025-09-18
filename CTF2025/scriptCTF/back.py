#!/usr/bin/env python3
# solve_socket_fix.py
# Chạy: python3 solve_socket_fix.py
import socket
import sys

HOST = "play.scriptsorcerers.xyz"
PORT = 10493
N = 100  # server dùng n = 100

def factor_count(x, p):
    cnt = 0
    while x % p == 0 and x > 0:
        x //= p
        cnt += 1
    return cnt

def compress(states):
    """
    states: list of (total2, total5).
    Trả về danh sách frontier không bị chi phối,
    sorted by total2 descending, và total5 strictly increasing along the list.
    """
    if not states:
        return []
    # giữ max total5 cho mỗi total2
    d = {}
    for a, b in states:
        prev = d.get(a)
        if prev is None or b > prev:
            d[a] = b
    items = sorted(d.items(), key=lambda x: -x[0])  # theo total2 giảm dần
    res = []
    max_b = -1
    for a, b in items:
        if b > max_b:
            res.append((a, b))
            max_b = b
    return res

def solve_grid(grid):
    n = len(grid)
    # tính cnt2, cnt5
    cnt2 = [[factor_count(grid[i][j], 2) for j in range(n)] for i in range(n)]
    cnt5 = [[factor_count(grid[i][j], 5) for j in range(n)] for i in range(n)]

    # frontier[i][j] là list các (total2, total5) không bị chi phối cho ô đó
    frontier = [[None]*n for _ in range(n)]
    # ô (0,0)
    frontier[0][0] = compress([(cnt2[0][0], cnt5[0][0])])

    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            states = []
            if i > 0 and frontier[i-1][j]:
                add2 = cnt2[i][j]; add5 = cnt5[i][j]
                for a,b in frontier[i-1][j]:
                    states.append((a + add2, b + add5))
            if j > 0 and frontier[i][j-1]:
                add2 = cnt2[i][j]; add5 = cnt5[i][j]
                for a,b in frontier[i][j-1]:
                    states.append((a + add2, b + add5))
            frontier[i][j] = compress(states)

    # tạo ma trận kết quả trailing zeros (max min(total2,total5) trên frontier)
    res = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            best = 0
            for a,b in frontier[i][j]:
                tz = a if a < b else b
                if tz > best:
                    best = tz
            res[i][j] = best
    return res

def read_grid_from_socket(s, n=N):
    """
    Đọc chính xác n dòng có số, bỏ qua dòng rỗng.
    Trả về list[string] n dòng.
    """
    buf = b""
    lines = []
    while len(lines) < n:
        chunk = s.recv(8192)
        if not chunk:
            break
        buf += chunk
        while b"\n" in buf and len(lines) < n:
            line, buf = buf.split(b"\n", 1)
            line_str = line.decode(errors="ignore").strip()
            if not line_str:
                continue
            # dòng có ít nhất một chữ số -> coi là dòng dữ liệu
            if any(ch.isdigit() for ch in line_str):
                lines.append(line_str)
    if len(lines) < n:
        raise RuntimeError(f"Chỉ nhận được {len(lines)} dòng (cần {n})")
    # parse to ints
    grid = [list(map(int, ln.split())) for ln in lines[:n]]
    return grid

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((HOST, PORT))

        # Đọc grid 100x100 từ server
        grid = read_grid_from_socket(s, N)

        # Giải
        ans = solve_grid(grid)

        # Gửi output (100 dòng)
        out = []
        for row in ans:
            out.append(" ".join(map(str, row)))
        out_bytes = ("\n".join(out) + "\n").encode()
        s.sendall(out_bytes)

        # Nhận phản hồi
        try:
            s.settimeout(5)
            resp = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
            if resp:
                print(resp.decode(errors="ignore"))
        except socket.timeout:
            pass

        s.close()
    except Exception as e:
        print("Lỗi:", e, file=sys.stderr)

if __name__ == "__main__":
    main()
