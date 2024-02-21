import axios from "axios";
import readCookie from "./readCookie.js";
import Toastify from "toastify-js";
let timerUpButton;
let timerDownButton;
let timerAmountSpan;
let timerAmount = 0;
let levelAmount = 1;
// current game id if no game is currently being played it is null
let gameID = null;
function showTimerAmount() {
  if (timerAmount !== 0) {
    timerAmountSpan.innerText = timerAmount;
    document.getElementById("sec_letters").style.display = "inline";
  } else {
    timerAmountSpan.innerText = "OFF";
    document.getElementById("sec_letters").style.display = "none";
  }
}

function setLevelAmount(e) {
  SaveSettingChange("level", e.target.dataset.level);
}
function showLevelAmount() {
  document
    .querySelectorAll(`[data-level]`)
    .forEach((button) => button.classList.remove("active"));
  document
    .querySelector(`[data-level='${levelAmount}']`)
    .classList.add("active");
}

function timerUp() {
  SaveSettingChange("timer", timerAmount + 10);
}

function timerDown() {
  if (timerAmount <= 0) {
    SaveSettingChange("timer", 0);
  } else {
    SaveSettingChange("timer", timerAmount - 10);
  }
}

function SaveSettingChange(setting, value) {
  if (gameID && setting === "timer") {
    axios.put(`/api/game/${gameID}/`, { [setting]: value });
  } else {
    axios.post("/api/settings/", { [setting]: value });
  }
  if (setting === "timer") {
    timerAmount = value;
    showTimerAmount();
  } else if (setting === "level") {
    levelAmount = value;
    showLevelAmount();
  }
}
function SetSettingsValues() {
  // get the backend saved settings. If the user is playing a game set the setting for the game,
  // If the user is not playing a game currently then just set the default users settings
  if (gameID) {
    // user is playing a game
    axios.get(`/api/game/${gameID}/`).then((response) => {
      timerAmount = response.data.timer;
      levelAmount = response.data.level;
      // update the displayed settings amount
      showTimerAmount();
      showLevelAmount();
    });
  } else {
    // user is not playing a game
    axios.get("/api/settings/").then((response) => {
      timerAmount = response.data.timer;
      levelAmount = response.data.level;
      // update the displayed settings amount
      showTimerAmount();
      showLevelAmount();
    });
  }
}

function showChangeLevelError() {
  Toastify({
    text: "Cannot change level during a game",
    backgroundColor: "info",
  }).showToast();
}

export default function loadSettingsPage() {
  timerDownButton = document.getElementById("timer_down");
  timerUpButton = document.getElementById("timer_up");
  timerAmountSpan = document.getElementById("timer_amount");

  timerUpButton.onclick = timerUp;
  timerDownButton.onclick = timerDown;
  if (readCookie("current_game")) {
    gameID = readCookie("current_game");
    document.querySelector(".button-section").onclick = showChangeLevelError;
  } else {
    // only allow user to update the level if not in middle of a game.
    document.querySelector(".button-section").classList.remove("disabled");
  }
  document
    .querySelectorAll(`[data-level]`)
    .forEach((button) => (button.onclick = setLevelAmount));
  SetSettingsValues();
}
