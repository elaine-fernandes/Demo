document.addEventListener('DOMContentLoaded', function() {
    console.log("Page loaded and script running!");
});

// Toggle the active class on the navbar when the menu icon is clicked
document.getElementById("menu-icon").onclick = function() {
    var navbar = document.querySelector(".navbar");
    navbar.classList.toggle("active");
};
;
