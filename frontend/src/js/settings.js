let timerUpButton;
let timerDownButton;
let timerAmountSpan;
let timerAmount = 0;
let levelAmount = 1;
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
    levelAmount = e.target.dataset.level
    showLevelAmount();
}
function showLevelAmount(){
    document.querySelectorAll(`[data-level]`).forEach(button=>button.classList.remove('active'))
    document.querySelector(`[data-level='${levelAmount}']`).classList.add('active')
}

function timerUp(){
    timerAmount+=10;
    showTimerAmount();
}

function timerDown(){
    timerAmount -=10;
    if (timerAmount<0){
        timerAmount = 0;
    }
    showTimerAmount();
}

export default function loadSettingsPage(){
    timerDownButton = document.getElementById("timer_down");
    timerUpButton = document.getElementById("timer_up");
    timerAmountSpan = document.getElementById("timer_amount");

    timerUpButton.onclick = timerUp;
    timerDownButton.onclick = timerDown;

    document.querySelectorAll(`[data-level]`).forEach(button=>button.onclick = setLevelAmount)
    showTimerAmount();
    showLevelAmount();
}