$(document).ready(function(e) {			
	t = $('.fixed').offset().top;
	mh = $('.mdcx').height();
	fh = $('.fixed').height();
	$(window).scroll(function(e){
		s = $(document).scrollTop();	
		if(s > t - 10){
			$('.fixed').css('position','fixed');
			$('.fixed').css('top',0);
			if(s + fh > mh){
				$('.fixed').css('top',mh-s-fh+'px');	
			}				
		}else{
			$('.fixed').css('position','');
			$('.fixed').css('top',100);
		}
	})
});
$(document).ready(function(e) {			
	t = $('.side').offset().top;
	mh = $('.mdcx').height();
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
			$('.side').css('top',80);
		}
	})
});