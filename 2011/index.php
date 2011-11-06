<?php
require('libs/Smarty.class.php');
require('libs/HTML.php');
require('util.php');

$page = $_GET['page'];
$titulos = get_pages();

if (!$page || !array_key_exists($page, $titulos)) {
    $page = 'index';
}

$smarty = new Smarty;
$smarty->assign('titulo', $titulos[$page]);
$html = $smarty->fetch($page.'.tpl');
$html = Minify_HTML::minify($html);
echo $html;
?>
