import axios from "axios";
import readCookie from "./readCookie.js";
import barba from "@barba/core";

function updateStatus(){
    axios.get(`/api/game/${readCookie('current_game')}/`).then(response=>{
        if(response.data.status==='Waiting for player to choose word'){
            setTimeout(()=>{
                updateStatus()
            },500)
        }else{
            barba.go('/game');
        }
    })
}

export default function loadWaitPage(){
    updateStatus();
}