
$(document).ready(function(e) {			
	t = $('.fixed').offset().top;/*71*/
	mh = $('.zc-content').height();/*1870*/
	fh = $('.fixed').height();/*0*/

	$(window).scroll(function(e){
		s = $(document).scrollTop();/*158*/

		if(s > t - 10){
			$('.fixed').css('position','fixed');
			$('.fixed').css('top',0);

			/*if(s + fh > mh){
				$('.fixed').css('top',mh-s-fh+'px');	
			}	*/
		}else{
			$('.fixed').css('position','');

		}
	})
});
$(document).ready(function(e) {			
	t = $('.side').offset().top;/*580*/
	mh = $('.zc-content').height();/*1870*/
	fh = $('.side').height();/*100*/

	$(window).scroll(function(e){
		s = $(document).scrollTop();
		if(s > t - 10){
			$('.side').css('position','fixed');
			$('.side').css('top',0);
			/*if(s + fh > mh){
				$('.side').css('top',mh-s-fh+'px');	
			}*/
		}else{
			$('.side').css('position','');
			$('.side').css('top',630);
		}
	})
});
