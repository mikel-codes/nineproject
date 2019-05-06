$(function($){
	/*
	$("input.reginput").each(function(){
		$(this).parent("form-group").removeClass("focused");
	});
	
	if ($("input.reginput").attr("autofocus", true))
		{	$("input.reginput").slice(0,1).parent(".form-group").addClass(".focused");}

	$("input.reginput").map(function(){
		if($(this).val() != "")
			$(this).parent("form-group").addClass(".focused");
	})
	*/
	$("input.reginput").blur(function(e){
		$(function () {
			console.log("blurred")
		});
		if ($(this).val() == "")
			console.log("ELement is empty")
			$(this).parent(".form-group").removeClass(".focused");

	})
	$("input.reginput").focus(function(e){
		//e.preventDefault()
		$(this).parent(".form-group").addClass(".focused");
	})


});


     	//$('[data-menu]').on('click', function(){
		
		//var mainMenu = $(this).data('menu');
		
		//$(mainMenu).toggleClass('visible-menu');
		
	

    	// SEARCH AREA
	if($('.src-btn')){
		
		var srcBtn = $('.src-btn');
		var srcIcn = $('.src-icn');
		var closeIcn = $('.close-icn');
		var srcForm = $('.src-form');
		
		srcBtn.on('click', function(){
			
			$(srcIcn).toggleClass('active');
			$(closeIcn).toggleClass('active');
			$(srcForm).toggleClass('active');
			
		});
	}



  // body...
 $(function($){
 	
     $("span#momentum").each(function(){
    var i = $(this).text();
    var m = moment(i.trim());
    $(this).text(m.fromNow());
 });
 })(jQuery);

