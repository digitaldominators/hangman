import axios from "axios";
import readCookie from "./readCookie.js";
let timerUpButton;
let timerDownButton;
let timerAmountSpan;
let timerAmount = 0;
let levelAmount = 1;
// current game id if no game is currently being played it is null
let gameID = null;
function showTimerAmount(){
    if(timerAmount!==0){
        timerAmountSpan.innerText = timerAmount;
        document.getElementById("sec_letters").style.display = 'inline'
    }else{
        timerAmountSpan.innerText = 'OFF'
        document.getElementById("sec_letters").style.display = 'none'
    }
}

function setLevelAmount(e){
    SaveSettingChange('level',e.target.dataset.level)
}
function showLevelAmount(){
    document.querySelectorAll(`[data-level]`).forEach(button=>button.classList.remove('active'))
    document.querySelector(`[data-level='${levelAmount}']`).classList.add('active')
}

function timerUp(){
    SaveSettingChange('timer',timerAmount+10)
}

function timerDown(){
    if(timerAmount<=0){
        SaveSettingChange('timer',0)
    }else{
        SaveSettingChange('timer',timerAmount-10)
    }
}

function SaveSettingChange(setting,value){
    if (gameID && setting==='timer'){
        axios.put(`/api/game/${gameID}/`,{[setting]:value});
    }else{
        axios.post("/api/settings/",{[setting]:value});
    }
    if(setting==='timer'){
        timerAmount = value;
        showTimerAmount();
    }else if(setting==='level'){
        levelAmount = value;
        showLevelAmount();
    }
}
function SetSettingsValues(){
    if (gameID){
        axios.get(`/api/game/${gameID}/`).then((response)=>{
            timerAmount = response.data.timer;
            levelAmount = response.data.level;
            showTimerAmount();
            showLevelAmount();
        })
    }else{
        axios.get("/api/settings/").then((response)=>{
            timerAmount = response.data.timer;
            levelAmount = response.data.level;
            showTimerAmount();
            showLevelAmount();
        })
    }

    showTimerAmount();
    showLevelAmount();
}

export default function loadSettingsPage(){
    timerDownButton = document.getElementById("timer_down");
    timerUpButton = document.getElementById("timer_up");
    timerAmountSpan = document.getElementById("timer_amount");

    timerUpButton.onclick = timerUp;
    timerDownButton.onclick = timerDown;
    if (readCookie("current_game")){
        gameID = readCookie("current_game");
    }else{
        // only allow user to update the level if not in middle of a game.
        document.querySelector('.button-section').classList.remove('disabled')
    }
    document.querySelectorAll(`[data-level]`).forEach(button=>button.onclick = setLevelAmount)
    SetSettingsValues();
}