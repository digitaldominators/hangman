import axios from "axios";
import readCookie from "./readCookie.js";
import barba from "@barba/core";
let category;
let phrase;
let active_player_name;
let active_player_score;
let second_player_score;
async function loadGameData(){
    let response = await axios.get(`/api/game/${readCookie('current_game')}/`);
    // initial game setup
    category.innerText = response.data.category;
    active_player_score.innerText = response.data.game_score;
    if (second_player_score){
        second_player_score.innerText = response.data.other_player_game_score;
    }

    // todo show the current players name
    let letters = "";
    for (let letter of response.data.word){
        letters += `<li class="letter guessed">${letter}</li>`
    }
    phrase.innerHTML = letters;

    if(response.data.is_multiplayer){
        setTimeout(()=>{
            getSecondPlayerData();
        },1000)
    }
}

function getSecondPlayerData(){
    axios.get(`/api/game/${readCookie('current_game')}/`).then(response=>{
        displayGameData(response.data);
        if(response.data.status==='you won' || response.data.status=== 'you lost'){
            return
        }
        setTimeout(()=>{
            getSecondPlayerData();
        },1000)
    }).catch(()=>{
        setTimeout(()=>{
            getSecondPlayerData();
        },1000)
    })
}
function displayGameData(data){
    active_player_score.innerText = data.game_score;

    if (document.getElementById('turn')){
        if (data.status==='not your turn'){
            document.getElementById('turn').innerText="WAITING FOR OTHER PLAYER"
        }else{
            document.getElementById('turn').innerText="";
        }
    }
    if (second_player_score){
        second_player_score.innerText = data.other_player_game_score;
    }
    // show data that constantly updates
    for (let i in data.word){
        // if the letter is different animate in the new correct letter
        if(phrase.children[i].innerText.toUpperCase()!==data.word[i].toUpperCase()){
            phrase.children[i].classList.add('adding');
            phrase.children[i].innerText = data.word[i];
            setTimeout(()=>{
                phrase.children[i].classList.remove('adding');
            },500)
        }
    }

    if(data.status==='you won'){
        setTimeout(()=>{
            barba.go('/youwon')
        },1000)
    }

    if(data.status==='you lost'){
        setTimeout(()=>{
            barba.go('/youlost')
        },1000)
    }
}

function guessLetter(e){
    let value = e.target.innerText;
    // console.log(e.target.innerText)
    axios.put(`/api/game/${readCookie('current_game')}/`,{guess:value}).then(response=>{
        displayGameData(response.data);
    })
}


export default function loadGamePage(){
    loadGameData();
    category = document.getElementById("category");
    phrase = document.getElementById("phrase");
    active_player_name = document.getElementById("active_player_name");
    active_player_score = document.getElementById("active_player_score");
    second_player_score = document.getElementById("second_player_score");


    for (let item of document.getElementsByClassName('letter-button')){
        item.onclick = guessLetter;
    }
}