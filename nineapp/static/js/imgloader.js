let imgsToLoad = document.querySelectorAll("img[data-src]")

const loadImages = (img) => {
  try {
    //console.log("From src", img.src)
    console.log("Data src", img['data-src'])
    console.log("Data src 3", img.dataset.src);
    let o = img.getAttribute('data-src')
    console.log("o says => ", img)
    //img.src = img.getAttribute('data-src')
    //img.setAttribute('src', img.getAttribute('data-src'))
    if(img.getAttribute('data-src') != ""){
      img.setAttribute('src', img.getAttribute('data-src'))
      console.log()
    }
    img.onload = () => {
      img.removeAttribute('data-src')
    }
  }
  catch (e) {
    console.log("Errors Occurred in loadImages", e)
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
