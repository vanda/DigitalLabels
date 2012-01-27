jQuery(document).ready(function() {
    
    
    $('#img, #txt').each(function(){
        var wM = parseFloat($(this).find('li').css('margin-right')),
            w = $(this).find('li').outerWidth() + wM,
            wA = $(this).find('li.active').outerWidth() + wM;
        $(this).width(w*($(this).find('li:last-child').index()+1)+wA);
        this.hit = function(i){
            var t = 1024;
            $(this).find('li').removeClass('active');
            $(this).find('li:nth-child('+(i+1)+')').addClass('active');
            $(this).animate({'left':$(window).width()/2-((i*w)+(0.5*wA))}, t);
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
    
    $('#img, #txt').on('click', 'li', function(){
        var i = $(this).index();
        $('#img, #txt').each(function(){ this.hit(i); });
    });
    
    $('#img').on('click', '.active', function(e){console.log(e.target);console.log(this);
        var pip = (e.target.tagName.toLowerCase()=='img')? e.target : $(this).find('img').get(0);
        $('#imgbig').attr('src',pip.src.replace(/_.+(\..+)$/,'$1'));
        $('#imgtxt').html(pip.title);
        $('#imgpop').css({'left':($(window).width()-$('#imgpop').outerWidth())/2}).show().mouseTrap({'mask':1});
    });
    
    $('#txt').on('click', '.active', function(){
        $('#txtpop').removeClass('home').html($(this).html()).css({'left':($(window).width()-$('#txtpop').outerWidth())/2}).show().mouseTrap({'mask':1});
        if( $(this).hasClass('home') ){ $('#txtpop').addClass('home'); }
    });
    
    $('.pop').on('click', function(){
        $('.pop').hide();
        $('#mousetrap').remove();
    });
    
    $('#img li.home').trigger('click');
    
    
}); //end doc.ready

/* plugins + fns */

/* Generic carini plugin for catching mouseclicks outside a JQ el */
(function($){
    $.fn.extend({
        mouseTrap: function(opt){
            var def = { close:this, mask:0 },
                opt = $.extend(def,opt);
            return this.each(function(){
                var obj = $(this);
                $('#mousetrap').remove();
                obj.before($('<div id="mousetrap" class="'+(opt.mask?'mask':'')+'"/>').click(function(){ $(opt.close).hide(); $('#mousetrap').remove(); }));
                obj.click(function(){ if( $(opt.close).is(':hidden') ){ $('#mousetrap').remove(); } });
            });
        }
    });
})(jQuery);
