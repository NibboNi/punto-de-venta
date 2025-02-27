const menuBtn = document.querySelector("#panel-menu-btn");
const dashboardNav = document.querySelector("#panel-nav");
const themeBtn = document.querySelector("#themeBtn");
const themeBtnText = document.querySelector("#themeBtn #themeBtnText");
let theme = localStorage.getItem("appTheme")
  ? localStorage.getItem("appTheme")
  : window.matchMedia("(prefers-color-scheme: dark)").matches
  ? "oscuro"
  : "claro";

if (!document.body.classList.contains("dark")) {
  if (theme === "oscuro") {
    document.body.classList.add("dark");
  }
}
localStorage.setItem("appTheme", theme);

if (themeBtn) {
  themeBtnText.textContent = theme;

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
}

if (menuBtn) {
  menuBtn.addEventListener("click", () => {
    if (dashboardNav.classList.contains("open")) {
      dashboardNav.classList.remove("open");
    } else {
      dashboardNav.classList.add("open");
    }
  });
}
