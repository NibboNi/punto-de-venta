const navBtn = document.querySelector("#menuBtn");
const headerNav = document.querySelector("#headerNav");

navBtn.addEventListener("click", () => {
  navBtn.classList.toggle("open");
  headerNav.classList.toggle("open");
});
