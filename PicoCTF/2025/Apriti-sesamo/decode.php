<?php

$username = $_POST['username'];
$pwd = $_POST['pwd'];

if ($username == $pwd) {
    echo "<br/>Failed! Ezaval identical successfully";
} else if (sha1($username) === sha1($pwd)) {
    echo file_get_contents("../flag{...}");
} else {
    echo "<br/>Failed! sha1 is equal but not same";
}
?>