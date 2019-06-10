/*
const isInViewport = (elem) => {
  var bounding = elem.getBoundingClientRect()
  return (
    bounding.top >= 0 && bounding.left >= 0 && bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
        )
}


const images = document.querySelectorAll('img')
window.onload = () => {
  window.addEventListener('scroll', (ev) => {

    Array.from(images).every(img => {
      //first load the thumbnail(LQIP)

      var thumb = new Image();
      thumb.src = img.dataset.src;
      console.log("This is a thumb image ",thumb)
      thumb.onload = () => 
        img.classList.add('placeholder .img.loaded img-small ')


      //load the complete version of the image now
      if (isInViewport(img)){
        console.log('im n viewport')
        var compImg = new Image()
        compImg.src = img.getAttribute('data-src')
        compImg.onload = () => {
          img.classList.remove('placeholder img-small')
          img.classList.add('img .img.loaded')
        }
      }
    })
  })
}
*/

/**

function fadeOutEffect() {
    var fadeTarget = document.getElementById("target");
    var fadeEffect = setInterval(function () {
       fadeTarget.style.transition = opacity 1s linear;
        if (!fadeTarget.style.opacity) {
            fadeTarget.style.opacity = 1;
        }
        if (fadeTarget.style.opacity > 0) {

            fadeTarget.style.opacity -= 0.1;
        } else {
            clearInterval(fadeEffect);
        }
    }, 200);
}
    
    console.log("This is this the bounding of the image", bounding)

  var elementBottom = elementTop + window.outerHeight();
  console.log("Element Top is ", elementTop)
  console.log("Element bottom is", elementBottom)

  
  var viewportTop = window.scrollTop();
  var viewportBottom = viewportTop + window.height();
  return elementBottom > viewportTop && elementTop < viewportBottom;
  

/**/
/**
<div class="placeholder" data-large="https://cdn-images-1.medium.com/max/1800/1*sg-uLNm73whmdOgKlrQdZA.jpeg">
  <img src="https://cdn-images-1.medium.com/freeze/max/27/1*sg-uLNm73whmdOgKlrQdZA.jpeg?q=20" class="img-small">
  <div style="padding-bottom: 66.6%;"></div>
</div>

   function showVisible() {
**/
      /*...Intermediate Code...*/
      
/**
      if ( Array.from(document.querySelectorAll('[data-src]')).every(
        img => img.getAttribute('data-src') === '') ) {
        window.removeEventListener('scroll', showVisible)
      }
    }




function preloadImg(event) {
  for (let img of wrapper.querySelectorAll('img')) {
    if (img.dataset.src && img.getBoundingClientRect().top + 100 < document.documentElement.clientHeight) {
      img.src = img.dataset.src;
      img.dataset.src = '';
    }
  }
}
**/

 // body...
  (function($){
    
     $("span#momentum").each(function(){
       console.log("we have span")
       var i = $(this).innerHTML;
       var m = moment(i.trim());
       $(this).text(m.fromNow());
  })
 }
 )(jQuery);

 (function($){
  
   
  $(".messages").delay(5000).slideUp(700);
    
      $('.go-top').on('click', function(e) {
        $('html, body').animate({scrollTop : 0},500);
  });


})(jQuery);

/*---LEFT BAR ACCORDION----*/





  //    sidebar dropdown menu auto scrolling

  jQuery('#sidebar .sub-menu > a').click(function() {
    var o = ($(this).offset());
    diff = 250 - o.top;
    if (diff > 0)
      $("#sidebar").scrollTo("-=" + Math.abs(diff), 500);
    else
      $("#sidebar").scrollTo("+=" + Math.abs(diff), 500);
  });



  //    sidebar toggle

  $(function() {
    function responsiveView() {
      var wSize = $(window).width();
      if (wSize <= 768) {
        $('#container').addClass('sidebar-close');
        $('#sidebar > ul').hide();
      }

      if (wSize > 768) {
        $('#container').removeClass('sidebar-close');
        $('#sidebar > ul').show();
      }
    }
    $(window).on('load', responsiveView);
    $(window).on('resize', responsiveView);
  });

  $('.fa-bars').click(function() {
    if ($('#sidebar > ul').is(":visible") === true) {
      $('#main-content').css({
        'margin-left': '0px'
      });
      $('#sidebar').css({
        'margin-left': '-210px'
      });
      $('#sidebar > ul').hide();
      $("#container").addClass("sidebar-closed");
    } else {
      $('#main-content').css({
        'margin-left': '210px'
      });
      $('#sidebar > ul').show();
      $('#sidebar').css({
        'margin-left': '0'
      });
      $("#container").removeClass("sidebar-closed");
    }
  });




  // widget tools

  jQuery('.panel .tools .fa-chevron-down').click(function() {
    var el = jQuery(this).parents(".panel").children(".panel-body");
    if (jQuery(this).hasClass("fa-chevron-down")) {
      jQuery(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
      el.slideUp(200);
    } else {
      jQuery(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
      el.slideDown(200);
    }
  });

  jQuery('.panel .tools .fa-times').click(function() {
    jQuery(this).parents(".panel").parent().remove();
  });




  // custom bar chart

  if ($(".custom-bar-chart")) {
    $(".bar").each(function() {
      var i = $(this).find(".value").html();
      $(this).find(".value").html("");
      $(this).find(".value").animate({
        height: i
      }, 2000)
    })
  }



    //    tool tips

  $('.tooltips').tooltip();

  //    popovers

  $('.popovers').popover();

  // Go to top



 
  