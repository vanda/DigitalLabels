jQuery(document).ready(function() {

    if( $(window).height()<710 && window.devicePixelRatio>1 ){
        var v = $('meta[name^="viewport"]'), 
            c = v.attr('content');
        v.attr('content', c.replace('initial-scale=1', 'initial-scale='+$(window).height()/710));
    }

    $(window).each(function(){
        $(this).on('resize', function(){
            $('#img>li.active').removeClass('active').trigger('click');
            $('.pop').each(function(){
                var l = ($(window).width()-$(this).outerWidth())/2;
                l = l>0? l:0;
                $(this).css('left',l);
            });
            $('#mousetrap').height($(document).height()).width($(document).width());
        });
    });

    $('#img, #txt').each(function(){
        if( $(this).children('.home').length < 1 ){ 
            $(this).children('li').eq(0).addClass('active'); 
        }else{ 
            $(this).children('.home').eq(0).addClass('active'); 
        }
        var i = $(this).children('li').not('.active'),
            w = i.outerWidth() + parseFloat(i.css('margin-left'))*2,
            iA = $(this).children('.active'),
            wA = iA.outerWidth() + parseFloat(iA.css('margin-left'))*2;
        $(this).children('.active').removeClass('active');
        $(this).width(w*($(this).children('li:last-child').index()+1)+wA);
        this.hit = function(i){
            $(this).stop();
            var t = 1024;
            $(this).children('.active>.mask').animate({'opacity':'0.5'}, t/4, null, $(this).children('li>.mask').show());
            $(this).animate({'left':$(window).width()/2-((i*w)+(0.5*wA))}, t, function(){
                $(this).children('li').removeClass('active').children('.mask').css({'opacity':'0.5','display':'block'});
                $(this).children('li:nth-child('+(i+1)+')').addClass('active').children('.mask').fadeToggle(t/4);
            });
        };
    });

    $('#img, #txt').on('click', 'li:not(.active)', function(){
        var i = $(this).index();
        $('#img, #txt').each(function(){ this.hit(i); });
        _gaq.push(['_trackEvent', 'Digital Labels (Furniture)', $(document).title, "Carousel Choice"]);
    });
    $('#img, #txt').children('li').each(function(){
        $(this).hammer({css_hacks:false, swipe:false, tap_double:false, hold:false}).on('dragstart', function(e){
            var li = $(this),
                a = Math.abs(e.angle);
            if( a<60 || a>150 ){
                if( li.is('.active') ){
                    $('#img, #txt').each(function(){
                        var d = (a<60? 1:-1);
                        var n = li.index()-d;
                        if( n>-1 && n<$(this).children('li').length ){ this.hit(n); }
                    });
                }else{
                    $('#img, #txt').each(function(){ this.hit($(li).index()); });
                }
               _gaq.push(['_trackEvent', 'Digital Labels (Furniture)', $(document).title, "Swipe"]);
               _gaq.push(['_trackEvent', 'Digital Labels (Furniture)', $(document).title, "Carousel Choice"]);
            }
        }).on('transform', function(e){
            if( $(this).is('.active') && e.scale>1 ){ $(this).trigger('click'); }
        });
    });

    $('#img').on('click', '.active', function(e){
        e.stopPropagation();
        var $pip = (e.target.tagName.toLowerCase()==='img')? $(e.target) : $(this).find('img'),
            l = ($(window).width()-$('#imgpop').outerWidth())/2;
        l = l>0? l:0;
        $('#imgbig').remove();
        $('#imgbox').prepend('<img id="imgbig" src="'+ $pip.data('img-l') +'" alt=""/>');
        $('#imgtxt').html($pip.data('caption'));
        $('#imgpop').css('left',l).show().mouseTrap({'mask':1});
        _gaq.push(['_trackEvent', 'Digital Labels', $(document).title, $pip.is('.active')?'Image Pop-up':'Secondary Image Pop-up']);
    });

    $('#txt').on('click', '.active', function(){
        var l = ($(window).width()-$('#txtpop').outerWidth())/2;
        l = l>0? l:0;
        $('#txtpop').removeClass('home').html($(this).html()).css('left',l).show().mouseTrap({'mask':1});
        if( $(this).hasClass('home') ){ $('#txtpop').addClass('home'); }
        _gaq.push(['_trackEvent', 'Digital Labels', $(document).title, 'Text Pop-up']);
    });

    $('.pop').hammer({css_hacks:false, swipe:false, tap_double:false, hold:false}).on('click transform', function(e){
        if( typeof(e.scale)==='undefined' || e.scale<1 ){
            $('.pop').hide();
            $('#mousetrap').remove();
        }
    });

    $('#img').each(function(){
        this.reset = function(){
            $('.pop').trigger('click');
            if( $(this).children('.find').length > 0 ){
                $(this).children('.find:not(.active)').trigger('click');
            }else if( $(this).children('.home').length > 0 ){
                $(this).children('.home').eq(0).not('.active').trigger('click');
            }else{
                $(this).children('li').eq(Math.floor($(this).children('li').length/2)).not('.active').trigger('click');
            }
        };
        this.reset();
    });

    $('#timeout').each(function(){
        var to = this, t,
            e = 4000, d = 80000;
        this.init = function(){
            $(this).show();
            $('#img').get(0).reset();
            if( $(this).children('img').length>1 ){ t = setTimeout(function(){ to.flick(); }, e); }
        };
        this.flick = function(){
            $(this).append($(this).children(':first-child').css({'opacity':0}).animate({'opacity':1}, 1000));
            t = setTimeout(function(){ to.flick(); }, e);
        };
        this.reset = function(){
            clearTimeout(t);
            $(this).hide();
            t = setTimeout(function(){ to.init(); }, d);
        };
        $(window).on('mousedown', function(e){ to.reset(); e.preventDefault(); });
        $('html').css({'cursor':'none'});
        this.init();
    });

}); //end doc.ready

/* plugins + fns */

/* Generic carini plugin for catching mouseclicks outside a JQ el */
(function($){
    $.fn.extend({
        mouseTrap: function(opt){
            var def = { close:this, mask:0 };
            opt = $.extend(def,opt);
            return this.each(function(){
                var obj = $(this);
                $('#mousetrap').remove();
                obj.before($('<div id="mousetrap" class="'+(opt.mask?'mask':'')+'"/>').height($(document).height()).width($(document).width()).on('click', function(){ $(opt.close).hide(); $('#mousetrap').remove(); }));
                obj.click(function(){ if( $(opt.close).is(':hidden') ){ $('#mousetrap').remove(); } });
            });
        }
    });
})(jQuery);
