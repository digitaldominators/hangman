import axios from "axios";
import barba from "@barba/core";
let form;
let username;
let password;
let password2;
let error_message;
function sign_up_user(e) {
  e.preventDefault();

  // get the form's data
  const formData = new FormData(sign_up_form);

  axios
    .post("/api/accounts/register/", {
      username: formData.get("username"),
      password: formData.get("password"),
      password2: formData.get("password2"),
    })
    .then((response) => {
      error_message.innerText = "";
      barba.go("/index");
    })
    .catch((error) => {
      if (error.response.data.error) {
        error_message.innerText = error.response.data.error;
      }
      if (error.response.data.username) {
        error_message.innerText = error.response.data.username;
      }
    });
}

export default function loadSignupPage() {
  form = document.getElementById("sign_up_form");
  username = document.getElementById("username_box");
  password = document.getElementById("password_box");
  password2 = document.getElementById("password2_box");
  error_message = document.getElementById("error_message");
  username.focus();
  form.onsubmit = sign_up_user;
}
