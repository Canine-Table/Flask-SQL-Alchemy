#!/usr/bin/node

const navbar = $("#navigationBar");

// Get the offset position of the navbar
let sticky = navbar.offset().top + 10;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function stickyNavbar() {
    if ($(window).scrollTop() >= sticky) {
        navbar.removeClass("fgc");
        navbar.addClass("bg-dark")
    } else {
        navbar.addClass("fgc")
        navbar.removeClass("bg-dark");
    }
}

// When the user scrolls the page, execute stickyNavbar
$(window).on("scroll", stickyNavbar);

