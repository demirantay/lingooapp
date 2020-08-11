// DOM Elements
var hidden_nav = document.getElementById("hidden_more_nav");
var toggle_button = document.getElementById("hidden-nav-toggle-button");

// toggling the hidden navigation
toggle_button.addEventListener("click", toggle_hidden_nav);

function toggle_hidden_nav(event) {
  event.preventDefault();

  /* added the or hidden nav equals to empty string because
  for some reason, (probably loading priorty of css and js the values are set)
  to empty so if it initialises block than it can innitilise none  */
  if (hidden_nav.style.display === "none" || hidden_nav.style.display === "") {
    hidden_nav.style.display = "block";
  } else if (hidden_nav.style.display === "block") {
    hidden_nav.style.display = "none";
  } else {
    alert("something is working wrong!");
  }

}
