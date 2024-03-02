import axios from "axios";
import barba from "@barba/core";
import {setCookie} from "./readCookie.js";

let password_form;
let logout_form;
let password;
let password2;
let error_message;
let showOnLeaderboardSwitch;
let popup_error_message;

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

function updateShowOnLeaderboard() {
  axios.post("/api/settings/", {
    private: !showOnLeaderboardSwitch.checked,
  });
}

function loadAccountInfo() {
  axios.get("/api/accounts/user_authenticated/").then((response) => {
    if (response.data.authenticated === false) {
      barba.go("/login");
    } else {
      // set username
      document.getElementById("username_box").innerHTML =
        response.data.username;
      document.getElementById("total_score_box").innerHTML =
        response.data.total_score;
      document.getElementById("average_score_box").innerHTML =
        response.data.average_score;
      document.getElementById("games_played_box").innerHTML =
        response.data.total_games;
      showOnLeaderboardSwitch.checked = response.data.show_leaderboard;
    }
  });
}

function displayRecentGames() {
  axios.get("api/game/").then((response) => {
    if (Object.keys(response.data).length) {
      createTable(response.data)
    } else {
      document.getElementById("popup_error_message").innerHTML =
        "You have not played any games yet";
    }
  });
}

function createTable(data) {
  const table = document.createElement('table');
  table.setAttribute('id', 'game_history_table');
  const tableHead = document.createElement('thead');
  const tableBody = document.createElement('tbody');
  const columnNames = ['Word', 'Status', 'Score', 'Level', 'Multiplayer'];
  const gameFields = ['word', 'status', 'game_score', 'level', 'is_multiplayer'];

  // Append the table head and body to the table
  table.appendChild(tableHead);
  table.appendChild(tableBody);

  // Create table head
  let row = tableHead.insertRow();
  columnNames.forEach(name => {
    let column = document.createElement('th');
    column.textContent = name;
    row.appendChild(column);
  })

  // Create table body
  data.forEach(game => {
    let gameSlug = game['game_slug'];
    let multiplayer = game['is_multiplayer'];
    let row = tableBody.insertRow();
    gameFields.forEach(column => {
      let cell = row.insertCell();
      if (column === 'status') {
        if (game[column] === 'you won' || game[column] === 'you lost') {
          cell.textContent = game[column];
        } else {
          let gameButton = document.createElement('button');
          gameButton.innerText = 'Continue';
          gameButton.setAttribute('class', 'game-history-button');
          gameButton.addEventListener('click', () => {
            redirectGame(gameSlug, multiplayer);
          });
          cell.appendChild(gameButton);
        }
      } else {
        cell.textContent = game[column];
      }
    })
  });

  // Append the table to the HTML document
  const closeButton = document.getElementById('close_button');
  document.getElementById('recent_games_dialog').insertBefore(table, closeButton);
}

function redirectGame(gameSlug, multiplayer) {
  setCookie("current_game", gameSlug, 100);
  if (multiplayer) {
    barba.go('/multigame');
  } else {
    barba.go('/game');
  }
}

export default function loadAccountPage() {
  password_form = document.getElementById("password_form");
  logout_form = document.getElementById("logout_form");
  password = document.getElementById("password_box");
  password2 = document.getElementById("password2_box");
  error_message = document.getElementById("error_message");
  showOnLeaderboardSwitch = document.getElementById("show_on_leaderboard");
  showOnLeaderboardSwitch.onchange = updateShowOnLeaderboard;
  password_form.onsubmit = change_password;
  logout_form.onsubmit = logout;

  popup_error_message = document.getElementById("popup_error_message");

  const dialog = document.getElementById("recent_games_dialog");
  document.getElementById("recent_games_button").addEventListener("click", () => {
    displayRecentGames();
    dialog.showModal();
  });

  const closeButton = document.getElementById("close_button");
  closeButton.addEventListener("click", () => {
    dialog.close();
    const table = document.getElementById('game_history_table');
    if (table) {
      table.remove();
    }
  });

  loadAccountInfo();
}
