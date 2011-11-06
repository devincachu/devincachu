(function(global, $) {

    $(global.document).ready(function(){
        $('.speakers').hide();
        $('.speaker_img').click(function(){
            $('.speakers').hide();
            var id = $(this).attr('id');
            id = '#speaker-' + id;
            $(id).fadeIn("slow");
        });
    });

    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-8088829-10']);
    _gaq.push(['_trackPageview']);

    (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();

})(this, this.jQuery);
