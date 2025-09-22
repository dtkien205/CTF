<?php
require __DIR__ . '/vendor/autoload.php';
require_once 'config.php'; 

if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
    header("Location: login.php");
    exit();
}

use Knp\Snappy\Pdf;

class PoC
{
    private $a;
    private $b;

    function __construct()
    {
        $this->a = 'date';
        $this->b = 'Y-m-d h:i:s';
    }

    function __wakeup()
    {
        $x = $this->a;
        $y = $this->b;
        return $x($y);
    }
}

$htmlContent = '';
$savePath = '';
$pdfMessage = '';
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $htmlContent = $_POST['htmlContent'] ?? '';
    $savePath = $_POST['savePath'] ?? '';

    if (empty($htmlContent)) {
        $pdfMessage = '<h1 class="warning">Vui lòng nhập mã HTML để tạo PDF.</h1>';
    } elseif (empty($savePath)) {
        $pdfMessage = '<h1 class="warning">Vui lòng nhập đường dẫn để lưu file PDF.</h1>';
    } else {
        $snappy = new Pdf('/usr/bin/wkhtmltopdf');
        try {
            $snappy->generateFromHtml($htmlContent, $savePath);
            $pdfMessage = '<h1 class="success">PDF được tạo thành công tại: ' . htmlspecialchars($savePath) . '</h1>';
        } catch (Exception $e) {
            $pdfMessage = '<h1 class="warning">Có lỗi xảy ra khi lưu file PDF.</h1>';
        }
    }
}
?>


?>
<!DOCTYPE html>
<html lang="vi">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Generate PDF</title>
    <link rel="stylesheet" href="styles.css" />
</head>

<body>
    <nav>
        <ul>
            <li><a href="index.php">Upload Ảnh</a></li>
            <li><a href="genPDF.php" class="active">Tạo PDF</a></li>
        </ul>
    </nav>
    <h1>Tạo PDF từ HTML</h1>
    <form action="genPDF.php" method="post">
        <textarea name="htmlContent" placeholder="Nhập mã HTML" rows="10" required><?php echo htmlspecialchars($htmlContent); ?></textarea>
        <input type="text" name="savePath" placeholder="Đường dẫn lưu file PDF" value="<?php echo htmlspecialchars($savePath ?? ''); ?>" required />
        <button type="submit">Tạo PDF</button>
    </form>
    <?php echo $pdfMessage; ?>
</body>

</html>