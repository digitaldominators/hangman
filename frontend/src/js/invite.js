import readCookie from "./readCookie.js";
import axios from "axios";
import barba from "@barba/core";

let invite_code;
let copied_message;

function updateStatus(){
    axios.get(`/api/game/${readCookie('current_game')}/`).then(response=>{
        if(response.data.status==='Waiting for player to join'){
            setTimeout(()=>{
                updateStatus()
            },500)
        }else{
            barba.go('/wait');
        }
    })
}

function copyInviteCode(){
    navigator.clipboard.writeText(readCookie("current_game"));
    copied_message.innerText = "Join Code Copied to clipboard";
    setTimeout(()=>{
        copied_message.innerText="";
    },1500)
}
export default function loadInvitePage(){
    invite_code = document.getElementById("invite_code");
    copied_message = document.getElementById("copied_message");

    invite_code.innerText = readCookie("current_game");

    invite_code.onclick = copyInviteCode;

    setTimeout(()=>{
        updateStatus()
    },500)
}