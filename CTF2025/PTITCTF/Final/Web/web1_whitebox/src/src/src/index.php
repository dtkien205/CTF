<?php

require_once 'config.php';

if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
    header("Location: login.php");
    exit();
}


$uploadMessage = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['image'])) {
    $file = $_FILES['image'];

    if ($file['error'] !== UPLOAD_ERR_OK) {
        $uploadMessage = '<h1 class="warning">Lỗi khi upload file.</h1>';
    } elseif ($file['size'] > 5 * 1024 * 1024) { // 5MB
        $uploadMessage = '<h1 class="warning">File vượt quá kích thước tối đa 5MB.</h1>';
    } else {
        $allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        $fileExtension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
        if (!in_array($file['type'], $allowedTypes) || strpos($fileExtension, 'php') !== false) {
            $uploadMessage = '<h1 class="warning">Chỉ chấp nhận các định dạng ảnh: JPEG, PNG, GIF.</h1>';
        } else {
            $uploadDir = 'uploads/';
            if (!is_dir($uploadDir)) {
                mkdir($uploadDir, 0755, true);
            }

            $filePath = $uploadDir . basename($file['name']);
            if (move_uploaded_file($file['tmp_name'], $filePath)) {
                $uploadMessage = '<h1 class="success">Upload thành công! File được lưu tại: ' . htmlspecialchars($filePath) . '</h1>';
            } else {
                $uploadMessage = '<h1 class="warning">Có lỗi xảy ra khi lưu file.</h1>';
            }
        }
    }
}
?>

<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Upload Ảnh</title>
    <link rel="stylesheet" href="styles.css" />
</head>

<body>
    <nav>
        <ul>
            <li><a href="index.php" class="active">Upload Ảnh</a></li>
            <li><a href="genPDF.php">Tạo PDF</a></li>
            <?php if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true): ?>
                <li><a href="logout.php">Đăng xuất (<?php echo htmlspecialchars($_SESSION['username']); ?>)</a></li>
            <?php else: ?>
                <li><a href="login.php">Đăng nhập</a></li>
                <li><a href="register.php">Đăng ký</a></li>
            <?php endif; ?>
        </ul>
    </nav>
    <h1>Upload Ảnh</h1>
    <form action="index.php" method="post" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required />
        <button type="submit">Upload</button>
    </form>
    <?php echo $uploadMessage; ?>
</body>

</html>