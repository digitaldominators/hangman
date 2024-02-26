import axios from "axios";
import readCookie, {setCookie} from "./readCookie.js";
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
    document.getElementById("level_section")
    .querySelectorAll(`[data-level]`)
    .forEach((button) => button.classList.remove("active"));
  document.getElementById("level_section")
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

  if(readCookie("character")==="skele"){
    document.getElementById("skele_button").classList.add('active');
  }else{
    document.getElementById("stick_button").classList.add('active');
  }

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

function changeCharacter(character) {
  document.getElementById("skele_button").classList.remove('active');
  document.getElementById("stick_button").classList.remove('active');
  document.getElementById(`${character}_button`).classList.add('active');
  setCookie('character', character, 100);
}

export default function loadSettingsPage() {
  timerDownButton = document.getElementById("timer_down");
  timerUpButton = document.getElementById("timer_up");
  timerAmountSpan = document.getElementById("timer_amount");

  timerUpButton.onclick = timerUp;
  timerDownButton.onclick = timerDown;
  if (readCookie("current_game")) {
    gameID = readCookie("current_game");
    document.querySelector("#level_section").onclick = showChangeLevelError;
  } else {
    // only allow user to update the level if not in middle of a game.
    document.querySelector("#level_section").classList.remove("disabled");
  }
  document.getElementById("level_section")
    .querySelectorAll(`[data-level]`)
    .forEach((button) => (button.onclick = setLevelAmount));
    document.getElementById("skele_button").onclick = () => {changeCharacter("skele")}
    document.getElementById("stick_button").onclick = () => {changeCharacter("stick")}
  SetSettingsValues();
}
