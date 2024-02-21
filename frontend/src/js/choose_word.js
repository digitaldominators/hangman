import axios from "axios";
import barba from "@barba/core";
import readCookie from "./readCookie.js";
import Toastify from "toastify-js";
let form;
let word_box;
function choose_word_game(e) {
  e.preventDefault();

  // get the forms data
  // data = word
  const formData = new FormData(form);

  axios
    .post(`/api/game/${readCookie("current_game")}/choose_word/`, {
      word: formData.get("word"),
    })
    .then((response) => {
      barba.go("/multigame");
    })
    .catch((error) => {
      word_box.select();
      word_box.focus();
    });
}

export default function loadChooseWordPage() {
  form = document.getElementById("choose_word_form");
  word_box = document.getElementById("word_box");
  word_box.focus();
  form.onsubmit = choose_word_game;
}
