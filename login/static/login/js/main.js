const themeBtn = document.querySelector("#themeBtn");
const themeBtnText = document.querySelector("#themeBtn .nav-link__text");
let theme = localStorage.getItem("appTheme")
  ? localStorage.getItem("appTheme")
  : window.matchMedia("(prefers-color-scheme: dark)").matches
  ? "oscuro"
  : "claro";

themeBtnText.textContent = theme;
if (!document.body.classList.contains("dark")) {
  if (theme === "oscuro") {
    document.body.classList.add("dark");
  }
}
localStorage.setItem("appTheme", theme);

themeBtn.addEventListener("click", () => {
  if (document.body.classList.contains("dark")) {
    document.body.classList.remove("dark");
    themeBtnText.textContent = "claro";
  } else {
    document.body.classList.add("dark");
    themeBtnText.textContent = "oscuro";
  }
  theme = themeBtnText.textContent;
  localStorage.setItem("appTheme", theme);
});
