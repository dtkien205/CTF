import socket

host = "chal2.fwectf.com"
ports = [4001, 8080, 1337, 80, 443, 3000, 5000, 8000, 8888]

for port in ports:
    try:
        s = socket.create_connection((host, port), timeout=2)
        print(f"[+] Port {port} is OPEN")
        s.close()
    except Exception:
        print(f"[-] Port {port} closed")
