

function fadeOutEffect(target) {
    var fadeTarget = document.getElementById(target);
    var fadeEffect = setInterval(function () {
       fadeTarget.style.transition = 'opacity 1s linear';
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


if (window.addEventListener && window.requestAnimationFrame && document.getElementsByClassName){
	window.addEventListener('load', ()  => {
		const img_targets = document.querySelectorAll('.placeholder')

		Array.from(img_targets).every(item => {
			console.log("Item is here", item)

			const loader = item.querySelector('.loader')
			const img    = item.querySelector('.img-small')
			window.addEventListener('scroll', scroller(img), false)
			window.addEventListener('resize', scroller(img), false);


			//first load the thumbnail(LQIP)
      		//load the complete version of the image now

      		try{
      			let img_elem = img;
      			console.log(img_elem)
      			if (isInViewport(img)){
      				let img2load = new Image()
      				img2load.src = img.getAttribute('data-src')
      				img.dataset.src = "";
      				img.setAttribute('data-src') = ''

      				console.log(img2load)
      				img2load.onload = () => {
      					console.log('started loading image')
      					img2load.className = 'card-img-top loaded'
      					console.log('added loaded class', main_img)

      					console.log('placeholder remove class')
      				}
      				placeholder.removeChild(loader)
      				placeholder.appendChild(img2load)
      			}
      			else
      				console.log("Nothing to load oo")
      		}
      		catch(error){
      			console.log("I found this error in ", error)
      		}
      	})
    })

}

const isInViewport = (elem) => {
  var bounding = elem.getBoundingClientRect()
  return (
    bounding.top >= 0 && bounding.left >= 0 && bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
        )
}


let isimginView = (img_elem) =>{
	if (img_elem != null){
		console.log(img_elem)
		//WT as window top and wB as window Bottom
		let wT = window.pageYOffset;
		let wB = wT + window.innerHeight;
		let pT, pB, p = 0;

		let cRect = img_elem.getBoundingClientRect();
		pT = wT + cRect.top;
		pB = wB + cRect.bottom;

	 	return ( wT < pB && wB > pT)
	 }

	 else
	 	console.log("From Image in view, still searching")


}


let scroller = (e, img) => {
	let timer;
	timer = timer || setTimeout(() =>{
		timer = null;
		requestAnimationFrame(isimginView(img))
	}, 300);
}

      		//item.appendChild(main_img)




      	/*
      	console.log("in viewport")
      	img.classList.remove('img-small')
      	img.src  = img.getAttribute('data-src')

        compImg.onload = () => {
          img.classList.remove('placeholder img-small')
          img.classList.add('img .img.loaded')
        }
        */


/*
if (window.addEventListener && window.requestAnimationFrame && document.getElementsByClassName)
	window.addEventListener('load', function() {

  // start
  var pItem = document.getElementsByClassName('progressive replace'), timer;

  window.addEventListener('scroll', scroller, false);
  window.addEventListener('resize', scroller, false);
  inView();


  // throttled scroll/resize
  function scroller(e) {

    timer = timer || setTimeout(function() {
      timer = null;
      requestAnimationFrame(inView);
    }, 300);

  }


  // image in view?
  function inView() {

    var wT = window.pageYOffset, wB = wT + window.innerHeight, cRect, pT, pB, p = 0;
    while (p < pItem.length) {

      cRect = pItem[p].getBoundingClientRect();
      pT = wT + cRect.top;
      pB = pT + cRect.height;

      if (wT < pB && wB > pT) {
        loadFullImage(pItem[p]);
        pItem[p].classList.remove('replace');
      }
      else p++;

    }

  }


  // replace with full image
  function loadFullImage(item) {

    if (!item || !item.href) return;

    // load image
    var img = new Image();
    if (item.dataset) {
      img.srcset = item.dataset.srcset || '';
      img.sizes = item.dataset.sizes || '';
    }
    img.src = item.href;
    img.className = 'reveal';
    if (img.complete) addImg();
    else img.onload = addImg;

    // replace image
    function addImg() {

      // disable click
      item.addEventListener('click', function(e) { e.preventDefault(); }, false);

      // add full image
      item.appendChild(img).addEventListener('animationend', function(e) {

        // remove preview image
        var pImg = item.querySelector && item.querySelector('img.preview');
        if (pImg) {
          e.target.alt = pImg.alt || '';
          item.removeChild(pImg);
          e.target.classList.remove('reveal');
        }

      });

    }

  }

}, false);



/*
window.onload = () => {
	const placeholder = document.querySelector('.placeholder')
	const  small = placeholder.querySelector('.img-small')

	// 1: load small image and show it
	var img = new Image();
	img.src = small.dataset.src;
	console.log('img', img)
	img.onload =  () => {
		small.classList.add('loaded');
	};

	// 2: load large image
	var imgLarge = new Image();
	imgLarge.src = placeholder.dataset.large;
	console.log('Image large ', imgLarge)
	imgLarge.onload =  () => {
		imgLarge.classList.add('loaded');
		console.log('image large', imgLarge)
	};
	placeholder.appendChild(imgLarge);
}


*/
