const deleteBtns = document.querySelectorAll(".delete-btn");
const modalContainerEl = document.querySelector("#modal-container");
const deleteBtn = document.querySelector("#deleteBtn");

deleteBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    modalContainerEl.classList.toggle("open");
    deleteBtn.href = deleteBtn.href.slice(0, -2) + btn.id;
  });
});

modalContainerEl.addEventListener("click", () => {
  modalContainerEl.classList.toggle("open");
});
