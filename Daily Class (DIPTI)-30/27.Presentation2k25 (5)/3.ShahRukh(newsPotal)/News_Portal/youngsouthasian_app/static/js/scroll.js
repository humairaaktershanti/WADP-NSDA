// script.js
document.addEventListener("DOMContentLoaded", () => {
    const dropdowns = document.querySelectorAll(".dropdown");
    dropdowns.forEach(drop => {
        drop.addEventListener("mouseenter", () => {
            drop.querySelector(".sub-menu").style.display = "block";
        });
        drop.addEventListener("mouseleave", () => {
            drop.querySelector(".sub-menu").style.display = "none";
        });
    });
});
