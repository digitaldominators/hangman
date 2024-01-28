import axios from "axios";
import barba from "@barba/core";
import {setCookie} from './readCookie.js'
let new_game_form;
let new_game_word_box;
let word_error_message;
function new_game_form_changed(e){
    // hide or show the word box when the multiplayer switch changes
    e.preventDefault();
    const formData = new FormData(new_game_form);
    if (formData.get("multiplayer")){
        new_game_word_box.style.opacity = 1;
        new_game_word_box.style.pointerEvents = 'auto'
    }else{
        new_game_word_box.style.opacity = 0;
        new_game_word_box.style.pointerEvents = 'none'
    }
}

function start_new_game(e){
    e.preventDefault();
    word_error_message.innerText = "";
    const formData = new FormData(new_game_form);
    let data= {
        // !! forces the value to be true or false and not null
        multiplayer:!!formData.get('multiplayer'),
    }
    if (data.multiplayer){
        data['word'] = formData.get("word")
    }
    axios.post("/api/game/",data).then(response=>{
        setCookie("current_game",response.data.game_slug,100);
        // redirect to the correct page.
        if(response.data.is_multiplayer){
            barba.go('/waiting');
        }else{
            barba.go('/game');
        }

    }).catch(error=>{
        if(error.response.data.word){
            word_error_message.innerText = error.response.data.word
        }
    });
}


export default function loadNewPage(){
    new_game_form = document.getElementById("new_game_form");
    new_game_word_box = document.getElementById("new_game_word");
    word_error_message = document.getElementById("word_error_message");

    new_game_form.onchange = new_game_form_changed;
    new_game_form.onsubmit = start_new_game;
}