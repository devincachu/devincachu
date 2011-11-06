<?php

function save_cached_content($content, $filename) {
    $fp = fopen(sprintf("/home/devincachu/static_devincachu/%s", $filename), "w");
    fprintf($fp, "%s", $content);
    fclose($fp);
    echo "Saved: ".$filename."<br />";
}

function get_pages() {
    $titulos = array(
            "quando-e-onde" => array("titulo" => "Quando e onde", "description" => "Local onde aconteceu o Dev in Cachu 2011", "keywords" => "devincachu, dev in cachu, s&atilde;o camilo, desenvolvimento de software, cachoeiro de itapemirim"),
            "programacao" => array("titulo" => "Programa&ccedil;&atilde;o", "description" => "Programa&ccedil;&atilde;o do Dev in Cachu 2011", "keywords" => "devincachu, dev in cachu, desenvolvimento de software, desenvolvimento, cachoeiro de itapemirim, programa&ccedil;&atilde;o, python, .net, java"),
            "palestrantes" => array("titulo" => "Palestrantes", "description" => "Palestrantes do Dev in Cachu 2011", "keywords" => "devincachu, dev in cachu, 2011, palestrantes, globo.com, caelum, giran, python, .net, cachoeiro de itapemirim, desenvolvimento, desenvolvedor"),
            "avaliacao" => array("titulo" => "Avalia&ccedil;&atilde;o", "description" => "Avalia&ccedil;&atilde;o do Dev in Cachu 2011", "keywords" => "devincachu, dev in cachu 2011, avalia&ccedil;&atilde;o, cachoeiro de itapemirim, desenvolvimento de software, desenvolvedor"),
            "patrocinio" => array("titulo" => "Patroc&iacute;nio", "description" => "Patroc&iacute;nio do Dev in Cachu 2011", "keywords" => "giran, caelum, globo.com, dataci, patrocinadores, devincachu, dev in cachu 2011, cachoeiro de itapemirim"),
            "caravanas" => array("titulo" => "Caravanas", "description" => "Caravanas para o Dev in Cachu 2011", "campos, alegre, campos dos goytacazes, ibira&ccedil;u, dev in cachu, cachoeiro de itapemirim, desenvolvimento de softwares"),
            "contato" => array("titulo" => "Contato", "description" => "Entre em contato com a organiza&ccedil;&atilde;o do Dev in Cachu 2011", "keywords" => "andressa agnhesi, isaura rangel, francisco souza, breno martinusso, magno machado, dev in cachu 2011, devincachu"),
            "index" => array("titulo" => "P&aacute;gina Inicial", "description" => "Dev in Cachu 2011 - evento de desenvolvedores de software no sul do Esp&iacute;rito Santo", "keywords" => "dev in cachu, devincachu, 2011, cachoeiro de itapemirim, desenvolvimento de software, carlos casteglione")
    );
    return $titulos;
}
