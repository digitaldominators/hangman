import axios from "axios";
import barba from "@barba/core";
import {setCookie} from "./readCookie.js";
let form;
let code_box;
let error_message;
function join_game(e){
    e.preventDefault();

    // get the forms data
    // data = game_slug
    const formData = new FormData(join_game_form);

    axios.post('/api/game/join_game/',{game_slug:formData.get("join_code")}).then(response=>{
        error_message.innerText = "";
        setCookie("current_game",formData.get("join_code"),100);
        barba.go('/choose_word');
    }).catch(error=>{
        code_box.select()
        code_box.focus()
        if (error.response.status===404){
            error_message.innerText = "Invalid join code"
            return
        }
        if(error.response.data.message){
            error_message.innerText = error.response.data.message
        }
    })
}


export default function loadJoinPage(){
    form = document.getElementById("join_game_form");
    code_box = document.getElementById("code_box")
    error_message = document.getElementById("error_message")
    code_box.focus()
    form.onsubmit = join_game;
}