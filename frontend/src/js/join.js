import axios from "axios";
import barba from "@barba/core";
import { setCookie } from "./readCookie.js";
let form;
let code_box;
function join_game(e) {
  e.preventDefault();

  // get the forms data
  // data = game_slug
  const formData = new FormData(join_game_form);

  axios
    .post("/api/game/join_game/", { game_slug: formData.get("join_code") })
    .then((response) => {
      setCookie("current_game", formData.get("join_code"), 100);
      barba.go("/choose_word");
    })
    .catch((error) => {
      code_box.select();
      code_box.focus();
    });
}

export default function loadJoinPage() {
  form = document.getElementById("join_game_form");
  code_box = document.getElementById("code_box");
  code_box.focus();
  form.onsubmit = join_game;
}
