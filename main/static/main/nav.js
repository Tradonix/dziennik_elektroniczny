document.addEventListener('DOMContentLoaded', () => {
    let toggleMenu = document.querySelector(".toggle-menu");
    let navTop = document.querySelector(".nav-top");

    toggleMenu.addEventListener("click", () => {
        navTop.classList.toggle("is-active");
    });
});
