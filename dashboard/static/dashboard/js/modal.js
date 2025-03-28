if (document.querySelector(".modal")) {
  const modal = document.querySelector(".modal");

  if (modal.classList.contains("show")) {
    setTimeout(() => {
      modal.classList.remove("show");
    }, 5000);
  }
}
