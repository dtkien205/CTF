<?php
session_start();

define('DB_SERVER', 'db');
define('DB_USERNAME', 'ctf_user');
define('DB_PASSWORD', 'ctf_password');
define('DB_NAME', 'ctf_db');

// Tạo kết nối PDO
try {
    $pdo = new PDO("mysql:host=" . DB_SERVER . ";dbname=" . DB_NAME, DB_USERNAME, DB_PASSWORD);
    // Đặt chế độ báo lỗi PDO thành Exception
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Lỗi kết nối cơ sở dữ liệu: " . $e->getMessage());
}
?>