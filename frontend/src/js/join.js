import readCookie from "./readCookie.js";
let join_game_form;
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
        })
        .catch((error)=>{
            alert("something went wrong")
        })
}


export default function loadJoinPage(){
    join_game_form = document.getElementById("join_game_form");

    join_game_form.onsubmit = join_game;
}