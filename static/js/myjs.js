
$(document).ready(function(e) {			
	t = $('.fixed').offset().top;
	mh = $('.zc-content').height();
	fh = $('.fixed').height();
	$(window).scroll(function(e){
		s = $(document).scrollTop();	
		if(s > t - 10){
			$('.fixed').css('position','fixed');
			$('.fixed').css('top',0);
			$('.zc-content').css('top',0);
			if(s + fh > mh){
				$('.fixed').css('top',mh-s-fh+'px');	
			}				
		}else{
			$('.fixed').css('position','');
			$('.zc-content').css('top',-150);
		}
	})
});
$(document).ready(function(e) {			
	t = $('.side').offset().top;
	mh = $('.zc-content').height();
	fh = $('.side').height();
	$(window).scroll(function(e){
		s = $(document).scrollTop();	
		if(s > t - 10){
			$('.side').css('position','fixed');
			$('.side').css('top',0);
			if(s + fh > mh){
				$('.side').css('top',mh-s-fh+'px');	
			}				
		}else{
			$('.side').css('position','');
			$('.side').css('top',480);
		}
	})
});
