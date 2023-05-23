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

const modal = document.querySelector(".modal_NTBT");
const trigger = document.querySelectorAll(".triggerModal");
const closeButton = document.querySelector(".close-button_NTBT");
const modalMainContent = document.querySelector(".contents_NTBT");

function toggleModal() {
  modal.classList.add("show-modal_NTBT");
  let child = this.cloneNode(true);
  modalMainContent.appendChild(child);
}

trigger.forEach((modalElement) => {
  modalElement.addEventListener("click", toggleModal);
});

closeButton.addEventListener(
  "click",
  () => {
    modal.classList.remove("show-modal_NTBT");
    modalMainContent.removeChild(modalMainContent.firstChild);
  },
  false
);
