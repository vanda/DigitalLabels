jQuery(document).ready(function() {

    if( $(window).height()<710 && window.devicePixelRatio>1 ){
        var v = $('meta[name^="viewport"]'), 
            c = v.attr('content');
        v.attr('content', c.replace('initial-scale=1', 'initial-scale='+$(window).height()/710));
    }

    $(window).each(function(){
        $(this).on('resize', function(){
            $('#img li.active').removeClass('active').trigger('click');
            $('.pop').each(function(){
                var l = ($(window).width()-$(this).outerWidth())/2;
                l = l>0? l:0;
                $(this).css('left',l);
            });
        });
    });
    
    $('#img, #txt').each(function(){
        if( $(this).find('li.home').length < 1 ){ 
            $(this).find('li').eq(0).addClass('active'); 
        }else{ 
            $(this).find('li.home').addClass('active'); 
        }
        var i = $(this).find('li').not('.active'),
            w = i.outerWidth() + parseFloat(i.css('margin-left'))*2,
            iA = $(this).find('li.active'),
            wA = iA.outerWidth() + parseFloat(iA.css('margin-left'))*2;
        $(this).find('li.active').removeClass('active');
        $(this).width(w*($(this).find('li:last-child').index()+1)+wA);
        this.hit = function(i){
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
        $(this).hammer({prevent_default:true, css_hacks:false, drag_vertical:false, swipe_min_distance:0}).on('swipe', function(e){
            var li = $(this);
            if( li.is('.active') ){
                $('#img, #txt').each(function(){ 
                    var n = li.index() + (e.direction=='left' ? 1:-1);
                    if( n>-1 && n<$(this).find('li').length){
                        this.hit(n);
                    }
                });
            }else{
                $('#img, #txt').each(function(){ this.hit($(li).index()); });
            }
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
    
    $('.pop').on('click', function(){
        $('.pop').hide();
        $('#mousetrap').remove();
    });
    
    $('#img').each(function(){
        if( $(this).find('li.home').length < 1 ){ 
            $(this).find('li').eq(Math.floor($(this).find('li').length/2)).trigger('click'); 
        }else{ 
            $(this).find('li.home').trigger('click');
        }
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
                obj.before($('<div id="mousetrap" class="'+(opt.mask?'mask':'')+'"/>').height($(document).height()*2).width($(document).width()*2).click(function(){ $(opt.close).hide(); $('#mousetrap').remove(); }));
                obj.click(function(){ if( $(opt.close).is(':hidden') ){ $('#mousetrap').remove(); } });
            });
        }
    });
})(jQuery);
