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
        if( $(this).find('li.home').length < 1 ){ 
            $(this).find('li').eq(0).addClass('active'); 
        }else{ 
            $(this).find('li.home').eq(0).addClass('active'); 
        }
        var i = $(this).find('li').not('.active'),
            w = i.outerWidth() + parseFloat(i.css('margin-left'))*2,
            iA = $(this).find('li.active'),
            wA = iA.outerWidth() + parseFloat(iA.css('margin-left'))*2;
        $(this).find('li.active').removeClass('active');
        $(this).width(w*($(this).find('li:last-child').index()+1)+wA);
        this.hit = function(i){
            $(this).stop();
            var t = 1024;
            $(this).find('.active>.mask').animate({'opacity':'0.5'}, t/4, null, $(this).find('li>.mask').show());
            $(this).animate({'left':$(window).width()/2-((i*w)+(0.5*wA))}, t, function(){ 
                $(this).find('li').removeClass('active').find('.mask').css({'opacity':'0.5','display':'block'}); 
                $(this).find('li:nth-child('+(i+1)+')').addClass('active').find('.mask').fadeToggle(t/4); 
            });
        };
    });

    $('#img, #txt').on('click', 'li:not(.active)', function(){
        var i = $(this).index();
        $('#img, #txt').each(function(){ this.hit(i); });
    });
    $('#img, #txt').find('li').each(function(){
        $(this).hammer({css_hacks:false, swipe:false, tap_double:false, hold:false}).on('dragstart', function(e){
            var li = $(this),
                a = Math.abs(e.angle);
            if( a<60 || a>150 ){
                if( li.is('.active') ){
                    $('#img, #txt').each(function(){
                        var d = (a<60? 1:-1);
                        var n = li.index() - d;
                        if( n>-1 && n<$(this).find('li').length){
                            this.hit(n);
                        }
                    });
                }else{
                    $('#img, #txt').each(function(){ this.hit($(li).index()); });
                }
            }
        }).on('transform', function(e){
            if( $(this).is('.active') && e.scale>1 ){ $(this).trigger('click'); }
        });
    });

    $('#img').on('click', '.active', function(e){
        var pip = (e.target.tagName.toLowerCase()==='img')? e.target : $(this).find('img').get(0),
            l = ($(window).width()-$('#imgpop').outerWidth())/2;
        l = l>0? l:0;
        $('#imgbig').remove();
        $('#imgbox').prepend('<img id="imgbig" src="'+ $(pip).data('img-l') +'" alt=""/>');
        $('#imgtxt').html(pip.title);
        $('#imgpop').css('left',l).show().mouseTrap({'mask':1});
    });

    $('#txt').on('click', '.active', function(){
        var l = ($(window).width()-$('#txtpop').outerWidth())/2;
        l = l>0? l:0;
        $('#txtpop').removeClass('home').html($(this).html()).css('left',l).show().mouseTrap({'mask':1});
        if( $(this).hasClass('home') ){ $('#txtpop').addClass('home'); }
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
            if( $(this).find('li.find').length > 0 ){
                $(this).find('li.find:not(.active)').trigger('click');
            }else if( $(this).find('li.home').length > 0 ){
                $(this).find('li.home:not(.active)').eq(0).trigger('click');
            }else{
                $(this).find('li:not(.active)').eq(Math.floor($(this).find('li').length/2)).trigger('click');
            }
        };
        this.reset();
    });

    $('#timeout').each(function(){
        var to = this, t;
        this.init = function(){
            $(this).show().css({'opacity':0}).animate({'opacity':1}, 1000);
            if( $(this).children('img').length>1 ){ setTimeout(function(){to.flick();}, 4000); }
        };
        this.flick = function(){
            $(this).append($(this).children(':first-child').css({'opacity':0}).animate({'opacity':1}, 1000));
            t = setTimeout(function(){to.flick();}, 4000);
        };
        this.reset = function(){
            clearTimeout(t);
            $(this).hide();
            t = setTimeout(function(){to.init(); $('#img').get(0).reset();}, 8000);
        };
        $(window).on('mousedown', function(){to.reset();});
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
