// attach onclick and onsubmit to post form
document.addEventListener("DOMContentLoaded", function () {
  // if on the main page where the create post form is
  if (document.querySelector("#open-create-form") && document.querySelector("#create-form")) {
    document.querySelector("#open-create-form").onclick = toggle_create_form;
    document.querySelector("#create-form").onsubmit = create_post;
    }
  
  // if on the post page where the edit post button is
  if (document.querySelector(".edit-post")) {
    document.querySelectorAll(".edit-post").forEach(button => {
      button.onclick = edit_post;
    });
    document.querySelectorAll(".save-new-post").forEach(button => {
      button.onclick = save_new_post;
    });
  }

  // attach onclick to like/unlike buttons
  document.querySelectorAll(".like-post").forEach(button => {
    button.onclick = like_post;
  });
  document.querySelectorAll(".unlike-post").forEach(button => {
    button.onclick = unlike_post;
  });
});

let postId = null;
let postDiv = null;

// toggling the form
function toggle_create_form() {
  document.querySelector("#create-post-form").classList.toggle("d-block");
  document.querySelector("#open-create-form").classList.toggle("d-none");
  document.querySelector("#title").value = "";
  document.querySelector("#body").value = "";
}

// adding a new post
function create_post() {
  body = document.querySelector("#body").value;
  
  fetch("/create_post", {
    method: "POST",
    body: JSON.stringify({
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

// saving the edited post
function save_new_post() {
  body = document.querySelector(`#new-body-${postId}`).value;
  document.querySelector(`.post-body-${postId}`).innerHTML = body;

  fetch(`/edit_post/${postId}`, {
    method: "PUT",
    body: JSON.stringify({
      body: body,
    }),
  })
  .then((res) => res.json())
  .then((data) => {
    alert(data.message, "success");

    postDiv.querySelector(".new-body").classList.toggle("d-none");
    postDiv.querySelector(".post-body").classList.toggle("d-none");
    postDiv.querySelector(".edit-post").classList.toggle("d-none");
    postDiv.querySelector(".save-new-post").classList.toggle("d-none");

    postId = null;
    postDiv = null;
  });
  
  return false;
}

// editing a post
function edit_post(event) {
  if (postId === null) {
    // take the closest post div
    postDiv = event.target.closest(".post");

    // get the post id and set it to the global variable
    postId = postDiv.getAttribute("data-post-id");
    console.log(postId);

    // hide the post body and show the form
    postDiv.querySelector(".new-body").classList.remove("d-none");
    postDiv.querySelector(".post-body").classList.add("d-none");
    postDiv.querySelector(".edit-post").classList.add("d-none");
    postDiv.querySelector(".save-new-post").classList.remove("d-none");
  }

}


// alert function
function alert(message, type = "primary") {
  element = document.querySelector(".alert");
  element.innerHTML = message;
  element.classList.remove("d-none");
  element.classList.add(`alert-${type}`);
  setTimeout(function () {
    element.classList.add("d-none");
  }, 3000);
}

// like/unlike a post
const like_post = (event) => {
  const postId_like = event.target.closest(".post").getAttribute("data-post-id");

  // send a PUT req with postId to update likes db
  fetch(`/like_post/${postId_like}`, {
    method: "PUT",
  })
  .then((res) => res.json())
  .then((data) => {
    alert(data.message, "success");


    //update count
    const likes = event.target.closest(".post").getAttribute("data-post-likes");
    event.target.closest(".post").querySelector(".post-likes").innerHTML = parseInt(likes) + 1;

    document.querySelector(`.like-post-${postId_like}`).classList.toggle("d-none");
    document.querySelector(`.liked-${postId_like}`).classList.toggle("d-none");


  })
}
// TODO: 
const unlike_post = (event) => {}