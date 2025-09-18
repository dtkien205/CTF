from pwn import remote
from collections import defaultdict
import math

def longest_subseq(nums):
    counter = defaultdict(int)
    for x in nums:
        x = abs(x)
        if x <= 1:
            continue
        temp = x
        p = 2
        while p * p <= temp:
            if temp % p == 0:
                counter[p] += 1
                while temp % p == 0:
                    temp //= p
            p += 1 if p == 2 else 2  # bỏ qua số chẵn sau 2
        if temp > 1:
            counter[temp] += 1
    return max(counter.values()) if counter else 0

def main():
    # Kết nối tới server
    io = remote("play.scriptsorcerers.xyz", 10351)

    # Đọc tới khi gặp input (tuỳ format challenge, mình assume là list số)
    data = io.recvuntil(b"\n").decode().strip()
    print("[Server] Input:", data)

    # Parse dãy số
    nums = list(map(int, data.split()))

    # Tính kết quả
    ans = longest_subseq(nums)
    print("[+] Answer:", ans)

    # Gửi lại server
    io.sendline(str(ans).encode())

    # Nhận flag
    print(io.recvall().decode())

if __name__ == "__main__":
    main()
