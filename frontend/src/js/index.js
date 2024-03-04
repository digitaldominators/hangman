import {
  get_body_types,
  set_body_type,
  get_current_part_index,
  get_total_parts,
  draw_next_body_part,
  refreshCanvas,
} from "./stageCanvas.js";
import readCookie from "./readCookie.js";
import axios from "axios";
import barba from "@barba/core";
let body_type_index = 0;
function next_part() {
  if (get_current_part_index() >= get_total_parts()) {
    body_type_index += 1;
    set_body_type(get_body_types()[body_type_index % get_body_types().length]);
    refreshCanvas(0, "previewCanvas");
  }

  draw_next_body_part();
  if (
    window.location.pathname === "/index.html" ||
    window.location.pathname === "/"
  ) {
    setTimeout(() => {
      next_part();
    }, 700);
  }
}

function showCurrentGameNotification() {
  function goToGame() {
    axios.get(`/api/game/${readCookie("current_game")}/`).then((response) => {
      if (response.data.is_multiplayer) {
        barba.go("/multigame");
      } else {
        barba.go("/game");
      }
    });
  }
  if (readCookie("current_game")) {
    let notif = document.createElement("div");
    notif.innerHTML = "Game in progress &ensp;&ensp;&ensp;";
    notif.classList.add(
      "toastify",
      "on",
      "toastify-center",
      "max-w-[100%]",
      "absolute",
      "top-[70px]",
      "z-0",
      "cursor-auto",
      "py-1"
    );
    let button = document.createElement("button");
    button.classList.add("bg-green-700", "px-5", "py-3", "rounded");
    button.innerText = "Continue Playing";
    button.onclick = goToGame;
    notif.append(button);
    document.getElementsByTagName("main")[0].prepend(notif);
  }
}

export default function loadIndexPage() {
  refreshCanvas(0, "previewCanvas");
  setTimeout(() => {
    showCurrentGameNotification();
  });

  setTimeout(() => {
    next_part();
  }, 500);
}
