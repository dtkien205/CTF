import requests
import time

URL = "http://c01549ea1bb0411cbf59876c969807450.chal3.fwectf.com:8004/"  # thay bằng URL thật của server

buf = []
length = 0

while True:
    try:
        r = requests.get(URL)
        d = r.json()

        if d.get("pwned"):
            if length == 0:
                length = d["len"]
                buf = ["?"] * length

            if buf[d["pos"]] == "?":
                buf[d["pos"]] = d["char"]
                print("".join(buf))

            # Nếu hoàn thành flag thì thoát
            if "?" not in buf:
                print("\n[+] Flag:", "".join(buf))
                break
        else:
            # pwned = false → server chưa chịu leak → thử lại
            pass

        time.sleep(0.2)

    except Exception as e:
        print("Error:", e)
        time.sleep(1)
