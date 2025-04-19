// =============================
// StudySyncTeam Component Logic
// =============================

document.addEventListener("DOMContentLoaded", () => {
    // Toggle Navbar on mobile
    const burger = document.querySelector(".navbar-burger");
    const menu = document.querySelector(".navbar-menu");
    if (burger && menu) {
      burger.addEventListener("click", () => {
        burger.classList.toggle("is-active");
        menu.classList.toggle("is-active");
      });
    }
  
    // Theme Switcher (Dark Mode)
    const themeToggle = document.getElementById("theme-toggle");
    if (themeToggle) {
      themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        const isDark = document.body.classList.contains("dark-mode");
        localStorage.setItem("theme", isDark ? "dark" : "light");
      });
    }
  
    // Persist theme preference
    if (localStorage.getItem("theme") === "dark") {
      document.body.classList.add("dark-mode");
    }
  });
  