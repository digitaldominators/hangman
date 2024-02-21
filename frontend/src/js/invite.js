import readCookie from "./readCookie.js";
import axios from "axios";
import barba from "@barba/core";
import Toastify from "toastify-js";

let invite_code;

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
    Toastify({
        text: "Join Code Copied to clipboard",
        backgroundColor: "blue",
    }).showToast();
}
export default function loadInvitePage(){
    invite_code = document.getElementById("invite_code");

    invite_code.innerText = readCookie("current_game");

    invite_code.onclick = copyInviteCode;

    setTimeout(()=>{
        updateStatus()
    },500)
}