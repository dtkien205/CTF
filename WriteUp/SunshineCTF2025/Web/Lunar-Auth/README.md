# 2025 Sunshine CTF - Lunar Auth

Mô tả của challege:
```
Infiltrate the LunarAuth admin panel and gain access to the super secret FLAG artifact !
```

Tôi thử kiểm tra xem có tệp `/robots.txt` không. Kết quả trả về:
```
# tired of these annoying search engine bots scraping the admin panel page logins:

Disallow: /admin
```

Truy cập vào endpoint `/admin` ta thấy một trang login. Kiểm tra src code html ta thấy một đoạn js quan trọng:
```js
const real_username = atob("YWxpbXVoYW1tYWRzZWN1cmVk");
const real_passwd   = atob("UzNjdXI0X1BAJCR3MFJEIQ==");
```
Trông chúng có vẻ giống encode-base64 giờ ta thử decode thu được u`sername: alimuhammadsecured` và `passwd: S3cur4_P@$$w0RD!`. Login thành công và thấy flag:

![alt text](image.png)