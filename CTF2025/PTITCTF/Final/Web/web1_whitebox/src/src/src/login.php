<?php
require_once 'config.php';

$message = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = trim($_POST['username']);
    $password = $_POST['password'];

    if (empty($username) || empty($password)) {
        $message = '<h1 class="warning">Vui lòng điền đầy đủ tên đăng nhập và mật khẩu.</h1>';
    } else {
        try {
            $stmt = $pdo->prepare("SELECT id, username, password_hash FROM users WHERE username = :username");
            $stmt->bindParam(':username', $username);
            $stmt->execute();

            if ($stmt->rowCount() == 1) {
                $user = $stmt->fetch(PDO::FETCH_ASSOC);
                if (password_verify($password, $user['password_hash'])) {
                    $_SESSION['loggedin'] = true;
                    $_SESSION['user_id'] = $user['id'];
                    $_SESSION['username'] = $user['username'];

                    header("Location: index.php");
                    exit();
                } else {
                    $message = '<h1 class="warning">Tên đăng nhập hoặc mật khẩu không đúng.</h1>';
                }
            } else {
                $message = '<h1 class="warning">Tên đăng nhập hoặc mật khẩu không đúng.</h1>';
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
    <title>Đăng nhập</title>
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
                <li><a href="login.php" class="active">Đăng nhập</a></li>
                <li><a href="register.php">Đăng ký</a></li>
            <?php endif; ?>
        </ul>
    </nav>
    <h1>Đăng nhập</h1>
    <form action="login.php" method="post">
        <label for="username">Tên đăng nhập:</label>
        <input type="text" id="username" name="username" required />

        <label for="password">Mật khẩu:</label>
        <input type="password" id="password" name="password" required />

        <button type="submit">Đăng nhập</button>
    </form>
    <?php echo $message; ?>
</body>
</html>