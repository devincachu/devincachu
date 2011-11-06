<?php

require('libs/Smarty.class.php');
require('libs/HTML.php');
require('util.php');

$pages = get_pages();

$smarty = new Smarty;
$smarty->assign('root', 'http://img.devincachu.com.br');

foreach ($pages as $file => $vars) {
    foreach ($vars as $name => $value) {
        $smarty->assign($name, $value);
    }

    $html = Minify_HTML::minify($smarty->fetch($file.'.tpl'));
    save_cached_content($html, $file.'.html');
}
