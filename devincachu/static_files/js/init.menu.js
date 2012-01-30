(function(global, document) {
    if (global._ === undefined) {
        global._ = {};
    }

    global._.definirAtivo = function() {
        var i, path = global.location.href.replace(/\/$/, '').replace(/^http:\/\/.*\//, '');
        var re = new RegExp(path + '/$');
        var itens = document.querySelectorAll('.nav > li > a');
        for (i = 0; i < itens.length; i++) {
            if (re.test(itens[i].href)) {
                itens[i].parentNode.classList.add('active');
                break;
            }
        }
    };

    document.getElementsByTagName("body")[0].onload = global._.definirAtivo();
})(window, window.document);
