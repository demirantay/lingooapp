// DOM Elements
background_greying = document.getElementById("background-greying");
hidden_mobile_top_nav = document.getElementById("hidden-mobile-top-nav");
toggle_top_nav = document.getElementById("toggle-top-nav");

hidden_nav_close_btn = document.getElementById("hidden-nav-close-btn");
open_hidden_nav_btn = document.getElementById("open-hidden-nav-btn");

// open the hidden top navigation
open_hidden_nav_btn.addEventListener("click", open_hidden_navigation);

function open_hidden_navigation(event) {
  event.preventDefault();

  background_greying.style.display = "block";
  hidden_mobile_top_nav.style.display = "block";
}

// close the hidden top navigation
hidden_nav_close_btn.addEventListener("click", close_hidden_navigation);

function close_hidden_navigation(event) {
  event.preventDefault();

  background_greying.style.display = "none";
  hidden_mobile_top_nav.style.display = "none";
  toggle_top_nav.style.display = "block";
}
