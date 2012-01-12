jQuery(document).ready(function() {
    
    
    $('#img, #txt').each(function(){
        var wM = parseFloat($(this).find('li').css('margin-right')),
            w = $(this).find('li').outerWidth() + wM,
            wA = $(this).find('li.active').outerWidth() + wM;
        $(this).width(w*($(this).find('li:last-child').index()+2));
        this.hit = function(i){
            var t = 1024;
            $(this).find('li').removeClass('active');
            $(this).find('li:nth-child('+(i+1)+')').addClass('active');
            $(this).animate({'left':$('body').width()/2-((i*w)+(0.5*wA))}, t);
        };
        this.nudge = function(n){
            var i = $(this).find('.active').index() + n;
            this.hit(i);
        };
    });
    
    $('#txt').find('li').not(':first-child').each(function(){
        $(this).append($('<div class="prev"></div>').click(function(){ $('#img, #txt').each(function(){ this.nudge(-1); }); return false; }));
    });
    
    $('#txt').find('li').not(':last-child').each(function(){
        $(this).append($('<div class="next"></div>').click(function(){ $('#img, #txt').each(function(){ this.nudge(1); }); return false; }));
    });
    
    $('#img, #txt').find('li').each(function(){
        $(this).click(function(){
            var i = $(this).index();
            $('#img, #txt').each(function(){ this.hit(i); });
        });
    });
    
    $('#img li.home').click();
    
    
}); //end doc.ready

/* plugins + fns */

/* Generic carini plugin for catching mouseclicks outside a JQ object */
(function($){
    $.fn.extend({
        mouseTrap: function(opt){
            var def = { close:this, positionMe:1, mask:0 },
                opt = $.extend(def,opt);
            return this.each(function(){
                var obj = $(this);
                if( opt.positionMe ){ obj.css({'position':'relative'}); }
                $('#mousetrap').remove();
                obj.before($('<div id="mousetrap" class="'+(opt.mask?'mask':'')+'"/>').css({'height':$(window).height(),'width':$(window).width()}).click(function(){ $(opt.close).hide(); $('#mousetrap').remove(); }));
                obj.click(function(){ if( $(opt.close).is(':hidden') ){ $('#mousetrap').remove(); } });
            });
        }
    });
})(jQuery);
