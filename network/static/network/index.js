document.addEventListener("DOMContentLoaded", function () {
  if (document.querySelector("#open-create-form") && document.querySelector("#create-form")) {
    document.querySelector("#open-create-form").onclick = toggle_create_form;
    document.querySelector("#create-form").onsubmit = create_post;
    }
});

function toggle_create_form() {
  document.querySelector("#create-post-form").classList.toggle("d-block");
  document.querySelector("#open-create-form").classList.toggle("d-none");
  document.querySelector("#title").value = "";
  document.querySelector("#body").value = "";
}

function alert(message, type = "primary") {
  element = document.querySelector(".alert");
  element.innerHTML = message;
  element.classList.remove("d-none");
  element.classList.add(`alert-${type}`);
  setTimeout(function () {
    element.classList.add("d-none");
  }, 3000);
}

function create_post() {
  title = document.querySelector("#title").value;
  body = document.querySelector("#body").value;

  fetch("/create_post", {
    method: "POST",
    body: JSON.stringify({
      title: title,
      body: body,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      alert(data.message, "success");
      toggle_create_form();
    });

  return false;
}
