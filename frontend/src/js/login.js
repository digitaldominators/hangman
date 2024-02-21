import axios from "axios";
import barba from "@barba/core";
let form;
let username;
let password;
function login_user(e) {
  e.preventDefault();

  // get the form's data
  const formData = new FormData(login_form);

  axios
    .post("/api/accounts/login_user/", {
      username: formData.get("username"),
      password: formData.get("password"),
    })
    .then((response) => {
      barba.go("/account");
    });
}

export default function loadLoginPage() {
  form = document.getElementById("login_form");
  username = document.getElementById("username_box");
  password = document.getElementById("password_box");
  username.focus();
  form.onsubmit = login_user;
}
