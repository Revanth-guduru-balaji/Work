const containerOne = document.querySelector(".container_1");
const openLayout = document.querySelector("#openLayout");

function onCloseLayout(flag) {
  if (flag) {
    containerOne.style.display = "none";
    openLayout.style.display = "block";
  } else {
    containerOne.style.display = "block";
    openLayout.style.display = "none";
  }
}
