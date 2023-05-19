/********* feature/CloseOrOpenLayout *********/

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
  


/********** Modal **********/

const modal = document.querySelector(".modal");
const trigger = document.querySelectorAll(".triggerModal");
const closeButton = document.querySelector(".close-button");
const modalMainContent = document.querySelector(".contents");

function toggleModal() {
  modal.classList.add("show-modal");
  let child = this.cloneNode(true);
  modalMainContent.appendChild(child);
}

trigger.forEach((modalElement) => {
  modalElement.addEventListener("click", toggleModal);
});

closeButton.addEventListener(
  "click",
  () => {
    modal.classList.remove("show-modal");
    modalMainContent.removeChild(modalMainContent.firstChild);
  },
  false
);
