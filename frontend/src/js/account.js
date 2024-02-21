import axios from "axios";
import barba from "@barba/core";
let password_form;
let logout_form;
let password;
let password2;
let error_message;

function change_password(e) {
  e.preventDefault();

  // get the form's data
  const formData = new FormData(password_form);

  axios.post("/api/accounts/change_password/", {
    password: formData.get("password"),
    password2: formData.get("password2"),
  });
}

function logout(e) {
  e.preventDefault();

  axios.post("/api/accounts/logout_user/").then((response) => {
    barba.go("/");
  });
}

export default function loadAccountPage() {
  password_form = document.getElementById("password_form");
  logout_form = document.getElementById("logout_form");
  password = document.getElementById("password_box");
  password2 = document.getElementById("password2_box");
  error_message = document.getElementById("error_message");
  password_form.onsubmit = change_password;
  logout_form.onsubmit = logout;
}