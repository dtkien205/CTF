# Web - Puzzle

Trang web cung cấp một file `old.db` bằng cách truy cập vào endpoint `/db`, trong đó có thông tin về admin và bẻ được một hash admin cũ - nhưng vô dụng. Hướng giải như sau:

```python
@app.route('/confirm-register', methods=['POST'])
    ...
    role = request.form.get('role', '2')
    role_map = {
        '1': 'editor',
        '2': 'user',
    }
```

`POST /confirm-register` chấp nhận một trường `role`. Vì vậy tôi tạo một account và thay đổi `role=2` -> `role=1` (editor).

![alt text](image.png)

Thành công → tài khoản mới có quyền `editor`, lấy session của account editor vừa tạo để đăng nhập: 

![alt text](image-1.png)

Ta tiếp tục xem trong src:

```python
current_user = get_user_by_uuid(current_uuid)
if not current_user or current_user['role'] not in ('0', '1'):
    return jsonify({'error': 'Invalid user role'}), 403
...
c.execute("SELECT uuid, username, email, phone_number, role, password FROM users WHERE uuid = ?", (target_uuid,))
# trả về luôn cả 'password'
```

Endpoint `/users/<uuid>` trả về dữ liệu nhạy cảm (kể cả mật khẩu dạng plaintext) nếu account có quyển `admin` hoặc `editor`. Với quyền `editor`, chỉ cần biết `uuid` của ai đó là xem được `profile` và `password` của họ. Vấn đề là làm sao có `uuid` của `admin`.

Hàm accept collab không kiểm tra quyền (missing authorization), cho phép bất kỳ tài khoản nào gọi API để chấp nhận request và gây ra hành vi mà server thực hiện như admin đã accept.
```python
@app.route('/collab/accept/<string:request_uuid>', methods=['POST'])
def accept_collaboration(request_uuid):
    # Missing authorization check - any user can accept any request
    c.execute("SELECT * FROM collab_requests WHERE uuid = ?", (request_uuid,))
```

Vì vậy tôi sẽ tạo một collab request gửi tới admin: 

![alt text](image-2.png)

![alt text](image-3.png)

Gọi thẳng `POST /collab/accept/<request_uuid>` để tự chấp nhận lời mời đó

![alt text](image-4.png)

Sau khi `accept`, xem bài viết → lấy được `admin_uuid`.

![alt text](image-5.png)

Tiếp theo trích xuất credential admin qua `/users/<admin_uuid>`

![alt text](image-6.png)

Với session `editor` (đã có). Endpoint trả về cả password (plaintext). Lấy mật khẩu `admin` từ JSON trả về và tiến hành đăng nhập.

![alt text](image-7.png)

Thành công vào được tài khoản admin và truy cập endpoint `/data` ta có được hai file:
- `dbconnect.exe` – chương trình có mật khẩu hardcode trong mã nguồn
- `secrets.zip` – file zip mã hóa, chứa flag

![alt text](image-8.png)

Phân tích `dbconnect.exe` để lấy mật khẩu và dùng mật khẩu đó để mở file `data.txt` trong `secreet.zip` và lấy `flag`

![alt text](image-9.png)

![alt text](image-10.png)