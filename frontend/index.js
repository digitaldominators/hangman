import readCookie from "./readCookie.js";
const new_game_modal = document.getElementById("new_game_modal");
const join_game_modal = document.getElementById("join_game_modal");
const new_game_button = document.getElementById("new_game_button");
const join_game_button = document.getElementById("join_game_button");
const new_game_word_box = document.getElementById("new_game_word");
const new_game_form = document.getElementById("new_game_form");
const join_game_form = document.getElementById("join_game_form");
function show_new_game(){
    new_game_modal.showModal();
}

function show_join_game(){
    join_game_modal.showModal();
}

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
            new_game_modal.hide();
        })
        .catch((error)=>{
            alert("something went wrong")
    })
}

function join_game(e){
    e.preventDefault();
    const formData = new FormData(join_game_form);

    const data = {
        game_slug: formData.get('join_code'),
        word: formData.get("word")
    }

    fetch("/api/game/join_game/",{
        method:"POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            "X-CSRFToken": readCookie("csrftoken")
        },
        body:JSON.stringify(data)})
        .then(response=>response.json())
        .then((response)=>{
            alert(`Joined game`)
            join_game_modal.close();
        })
        .catch((error)=>{
            alert("something went wrong")
        })
}
window.onload = function() {
    new_game_button.onclick = show_new_game;
    join_game_button.onclick = show_join_game;
    new_game_form.onchange = new_game_form_changed;
    new_game_form.onsubmit = start_new_game;
    join_game_form.onsubmit = join_game;
}