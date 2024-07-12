document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#open-create-form").onclick = open_create_form;
  document.querySelector("#create-form").onsubmit = create_post;
});

function open_create_form() {
  document.querySelector("#create-post-form").className = "d-block";
  document.querySelector("#open-create-form").className = "d-none";
}

function create_post() {
  title = document.querySelector("#title").value;
  body = document.querySelector("#body").value;
}
