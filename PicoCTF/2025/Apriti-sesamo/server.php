<?php
if (isset($_POST[base64_decode("\144\130\x4e\154\x63\155\x35\x68\142\127\125\x3d")]) && isset($_POST[base64_decode("\143\x48\x64\x6b")])) {
    $x = $_POST[base64_decode("\144\x58\x4e\154\x63\x6d\65\150\x62\127\x55\75")];
    $y = $_POST[base64_decode("\143\x48\144\153")];
    if ($x == $y) {
        echo base64_decode("\x50\x47\112\x79\x4c\172\x35\x47\x59\127\154\163\132\127\x51\x68\111\x45\x35\166\x49\x47\132\163\131\127\x63\x67\x5a\155\71\171\111\x48\x6c\166\x64\x51\x3d\x3d");
    } else {
        if (sha1($x) === sha1($y)) {
            echo file_get_contents(base64_decode("\x4c\151\64\166\x5a\x6d\x78\x68\x5a\x79\65\60\145\110\x51\75"));
        } else {
            echo base64_decode("\x50\107\112\171\x4c\x7a\65\107\x59\x57\154\x73\x5a\127\x51\x68\x49\105\x35\x76\111\x47\132\x73\131\127\x63\x67\x5a\155\71\x79\x49\110\154\x76\x64\x51\x3d\75");
        }
    }
} ?>