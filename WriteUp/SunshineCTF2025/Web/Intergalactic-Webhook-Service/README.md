# 2025 Sunshine CTF - Intergalactic Webhook Service

Mô tả của challenge:
```
I got tired of creating webhooks from online sites, so I made my own webhook service! It even works in outer space! Be sure to check it out and let me know what you think. I'm sure it is the most secure webhook service in the universe.
```

Vì challenge cho src nên tôi sẽ liệt kê một số phần liên quan: 
```python
class FlagHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/flag':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(FLAG.encode())
        else:
            self.send_response(404)
            self.end_headers()

threading.Thread(target=lambda: HTTPServer(('127.0.0.1', 5001), FlagHandler).serve_forever(), daemon=True).start()
```

Phần này cho chúng ta biết rằng chúng ta có thể lấy flag bằng yêu cầu POST tới `http://127.0.0.1:5001/flag`. 

Có 2 endpoint liên quan: /register (đăng webhook) và /trigger (gọi webhook đã đăng). Cả hai đều gọi hàm is_ip_allowed(url) để chặn URL trỏ tới địa chỉ nội bộ.

Khi xem mã nguồn cho `/trigger`, tôi thấy mã bên dưới gửi POST request đến địa chỉ được chỉ định bởi webhook miễn là nó vượt qua các kiểm tra trong `is_ip_allowed(url)`.

Hàm kiểm tra `is_ip_allowed`
```python
def is_ip_allowed(url):
    parsed = urlparse(url)
    host = parsed.hostname or ''
    try:
        ip = socket.gethostbyname(host)
    except Exception:
        return False, f'Could not resolve host'
    ip_obj = ipaddress.ip_address(ip)
    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved:
        return False, f'IP "{ip}" not allowed'
    return True, None
```

- Lấy host từ URL bằng urllib.parse.urlparse.
- Resolve ra IP thật bằng socket.gethostbyname.
- Nếu IP nằm trong các dải nội bộ (127.0.0.1, 10.x, 192.168.x.x, …) → từ chối.

#### Điểm yếu
Hàm kiểm tra `is_ip_allowed` và hàm gửi `requests.post` không dùng cùng một parser URL.

    is_ip_allowed → urllib.parse.urlparse
    requests.post(url, ...) → urllib3 bên trong Requests

Nếu 2 parser hiểu URL khác nhau → parser differential (mỗi thằng nghĩ host là khác nhau). Đây chính là chỗ để bypass.

```python
def is_ip_allowed(url):
    parsed = urlparse(url)       # <-- đây dùng urllib.parse.urlparse
    host = parsed.hostname or '' # <-- hostname từ urlparse dùng để resolve
    try:
        ip = socket.gethostbyname(host)
    ...
```

```python
def trigger_webhook():
    ...
    try:
        resp = requests.post(url, timeout=5, allow_redirects=False)   # <-- đây dùng urllib3 bên trong Requests
    ...    
```

#### Ví dụ: `http://1.1.1.1&@2.2.2.2#@3.3.3.3/`
- `urllib2 / httplib` (cũ): nghĩ host là `1.1.1.1`
- `requests`: nghĩ host là `2.2.2.2`
- `urllib`: nghĩ host là `3.3.3.3`

#### Payload: `http://127.0.0.1:5001\@8.8.8.8/../flag`
- `urllib.parse` coi phần trước và sau `\@` là một `netloc` chung nhưng `hostname` cuối cùng được trả là phần sau (ở payload là 8.8.8.8).

- `urllib3` coi `\@` như escape/ký tự đặc biệt không phân tách `userinfo`, và nhận host thực là 127.0.0.1 với port 5001.

### Lấy flag:
![alt text](image.png)

