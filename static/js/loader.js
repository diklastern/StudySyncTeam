document.addEventListener("DOMContentLoaded", () => {
    const loader = document.createElement("div");
    loader.className = "pageloader is-active";
    document.body.appendChild(loader);
  
    setTimeout(() => {
      loader.classList.remove("is-active");
      setTimeout(() => loader.remove(), 600);
    }, 600);
  });
  