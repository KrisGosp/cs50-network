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

  fetch("/create_post", {
    method: "POST",
    body: JSON.stringify({
      title: title,
      body: body,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data.message);
      title = "";
      body = "";
      document.querySelector("#open-create-form").className = "d-block";
      document.querySelector("#create-post-form").className = "d-none";
    });

  return false;
}
