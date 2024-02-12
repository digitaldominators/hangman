import axios from "axios";
import barba from "@barba/core";
import readCookie from "./readCookie.js";
let form;
let word_box;
let error_message;
function choose_word_game(e){
    e.preventDefault();

    // get the forms data
    // data = word
    const formData = new FormData(form);

    axios.post(`/api/game/${readCookie("current_game")}/choose_word/`,{word:formData.get("word")}).then(response=>{
        error_message.innerText = "";
        barba.go('/multigame');
    }).catch(error=>{
        word_box.select()
        word_box.focus()
        if (error.response.status===404){
            error_message.innerText = "Invalid join code"
            return
        }
        if(error.response.data.message){
            error_message.innerText = error.response.data.message
        }
    })
}


export default function loadChooseWordPage(){
    form = document.getElementById("choose_word_form");
    word_box = document.getElementById("word_box")
    error_message = document.getElementById("error_message")
    word_box.focus()
    form.onsubmit = choose_word_game;
}