import axios from "axios";
import barba from "@barba/core";
import Toastify from "toastify-js";
let form;
let username;
let password;
let password2;
function sign_up_user(e) {
  e.preventDefault();

  // get the form's data
  const formData = new FormData(sign_up_form);
  const uninterceptedAxiosInstance = axios.create();
  uninterceptedAxiosInstance
    .post("/api/accounts/register/", {
      username: formData.get("username"),
      password: formData.get("password"),
      password2: formData.get("password2"),
    })
    .then((response) => {
      Toastify({
        text: "Account Created",
        backgroundColor: "green",
      }).showToast();
      barba.go("/account");
    })
    .catch((error) => {
      if (error.response.data.error) {
        Toastify({
          text: error.response.data.error,
          backgroundColor: "red",
        }).showToast();
      }
      if (error.response.data.username) {
        Toastify({
          text: error.response.data.username,
          backgroundColor: "red",
        }).showToast();
      }
    });
}

export default function loadSignupPage() {
  form = document.getElementById("sign_up_form");
  username = document.getElementById("username_box");
  password = document.getElementById("password_box");
  password2 = document.getElementById("password2_box");
  username.focus();
  form.onsubmit = sign_up_user;
}
