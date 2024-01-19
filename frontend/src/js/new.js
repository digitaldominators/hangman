import readCookie from "./readCookie.js";
let new_game_form;
let new_game_word_box;
function new_game_form_changed(e){
    e.preventDefault();
    const formData = new FormData(new_game_form);
    if (formData.get("single_player")){
        new_game_word_box.style.display = 'none'
    }else{
        new_game_word_box.style.display = 'inline'
    }
}

function start_new_game(e){
    e.preventDefault();
    const formData = new FormData(new_game_form);
    let data= {
        multiplayer:!formData.get('single_player'),
    }
    if (data.multiplayer){
        data['word'] = formData.get("word")
    }
    fetch("/api/game/",{
        method:"POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "X-CSRFToken": readCookie("csrftoken")
        },
        body:JSON.stringify(data)})
        .then(response=>response.json())
        .then((response)=>{
            alert(`the game slug is: ${response.game_slug}`)
        })
        .catch((error)=>{
            alert("something went wrong")
        })
}


export default function loadNewPage(){
    new_game_form = document.getElementById("new_game_form");
    new_game_word_box = document.getElementById("new_game_word");

    new_game_form.onchange = new_game_form_changed;
    new_game_form.onsubmit = start_new_game;
}