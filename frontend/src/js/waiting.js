import readCookie from "./readCookie.js";
import axios from "axios";
import barba from "@barba/core";
let join_code;
let title;
let join_section;
function updateStatus(){
    axios.get(`/api/game/${readCookie('current_game')}/`).then(response=>{
        if(response.data.status==='Waiting for player to join'){
            setTimeout(()=>{
                updateStatus()
            },500)
        }else if(response.data.status==='Waiting for player to choose word'){
            title.innerText = "Friend Joined!"
            join_section.innerText = "Choosing Word."
            setTimeout(()=>{
                updateStatus()
            },500)
        }else{
            barba.go('/game');
        }
    })
}

export default function loadWaitingPage(){
    join_code = document.getElementById("join_code");
    title = document.getElementById("title");
    join_section = document.getElementById('join_section');
    join_code.innerText = readCookie("current_game");

    setTimeout(()=>{
        updateStatus()
    },500)
}