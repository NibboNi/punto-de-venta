const btn = document.querySelector("#test");
const modal = document.querySelector(".modal");
btn.addEventListener("click", () => {
  modal.classList.add("show");
  setTimeout(() => {
    modal.classList.remove("show");
  }, 5000);
});
