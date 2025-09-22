<?php
require_once 'config.php'; // Chứa session_start() và kết nối DB

$message = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username']);
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];

    // 1. Kiểm tra đầu vào
    if (empty($username) || empty($password) || empty($confirm_password)) {
        $message = '<h1 class="warning">Vui lòng điền đầy đủ tất cả các trường.</h1>';
    } elseif ($password !== $confirm_password) {
        $message = '<h1 class="warning">Mật khẩu xác nhận không khớp.</h1>';
    } elseif (strlen($password) < 6) {
        $message = '<h1 class="warning">Mật khẩu phải có ít nhất 6 ký tự.</h1>';
    } else {
        try {
            // 2. Kiểm tra tên người dùng đã tồn tại chưa
            $stmt = $pdo->prepare("SELECT id FROM users WHERE username = :username");
            $stmt->bindParam(':username', $username);
            $stmt->execute();

            if ($stmt->rowCount() > 0) {
                $message = '<h1 class="warning">Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.</h1>';
            } else {
                // 3. Mã hóa mật khẩu
                $password_hash = password_hash($password, PASSWORD_DEFAULT);

                // 4. Lưu người dùng vào cơ sở dữ liệu
                $stmt = $pdo->prepare("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)");
                $stmt->bindParam(':username', $username);
                $stmt->bindParam(':password_hash', $password_hash);

                if ($stmt->execute()) {
                    $message = '<h1 class="success">Đăng ký thành công! Bạn có thể <a href="login.php">đăng nhập</a> ngay bây giờ.</h1>';
                } else {
                    $message = '<h1 class="warning">Có lỗi xảy ra khi đăng ký. Vui lòng thử lại.</h1>';
                }
            }
        } catch (PDOException $e) {
            $message = '<h1 class="warning">Lỗi kết nối hoặc truy vấn cơ sở dữ liệu: ' . $e->getMessage() . '</h1>';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Đăng ký</title>
    <link rel="stylesheet" href="styles.css" />
</head>
<body>
    <nav>
        <ul>
            <li><a href="index.php">Upload Ảnh</a></li>
            <li><a href="genPDF.php">Tạo PDF</a></li>
            <?php if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true): ?>
                <li><a href="logout.php">Đăng xuất (<?php echo htmlspecialchars($_SESSION['username']); ?>)</a></li>
            <?php else: ?>
                <li><a href="login.php">Đăng nhập</a></li>
                <li><a href="register.php" class="active">Đăng ký</a></li>
            <?php endif; ?>
        </ul>
    </nav>
    <h1>Đăng ký tài khoản mới</h1>
    <form action="register.php" method="post">
        <label for="username">Tên đăng nhập:</label>
        <input type="text" id="username" name="username" required />

        <label for="password">Mật khẩu:</label>
        <input type="password" id="password" name="password" required />

        <label for="confirm_password">Xác nhận mật khẩu:</label>
        <input type="password" id="confirm_password" name="confirm_password" required />

        <button type="submit">Đăng ký</button>
    </form>
    <?php echo $message; ?>
</body>
</html>