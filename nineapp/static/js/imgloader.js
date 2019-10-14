let imgsToLoad = document.querySelectorAll("img[data-src]")

const loadImages = (img) => {
  try {
    if(img.getAttribute('data-src') != ""){
      img.setAttribute('src', img.getAttribute('data-src'))

    }
    img.onload = () => {
      img.removeAttribute('data-src')
    }
  }
  catch (e) {
    console.log("Errors Occurred in loading images", e)
    return
  }
}


if('IntersectionObserver' in window){
  const observer = new IntersectionObserver((items, observer) => {
    items.forEach( (item) => {
      if(item.isIntersecting){
        loadImages(item.target);
        observer.unobserve(item.target);
      }
    })
  })
  imgsToLoad.forEach((image) => {
    observer.observe(image)
  })

}
else{
  imgsToLoad.forEach((image) => {
    loadImages(image)
  });
}
