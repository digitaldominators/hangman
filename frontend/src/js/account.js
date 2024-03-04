import axios from "axios";
import barba from "@barba/core";
let password_form;
let logout_form;
let password;
let password2;
let error_message;
let showOnLeaderboardSwitch;
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

  loadAccountInfo();
}
