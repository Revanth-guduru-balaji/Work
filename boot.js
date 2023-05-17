const containerOne = document.querySelector(".Imagecontainer");
const openLayout = document.querySelector("#openLayout");
function onCloseLayout(flag) {
    if (flag) {
      containerOne.style.display = "none";
      openLayout.style.display = "block";
      document.querySelector('.main').classList.add('full-width');
    } else {
      containerOne.style.display = "block";
      openLayout.style.display = "none";
      document.querySelector('.main').classList.remove('full-width');
    }
  }
  
