import axios from "axios";
import readCookie from "./readCookie.js";
import barba from "@barba/core";
import {gsap} from "gsap";
import confetti from './confetti.js'
let category;
let phrase;
let active_player_name;
let active_player_score;
let second_player_score;
let second_player_name;
async function loadGameData(){
    let response = await axios.get(`/api/game/${readCookie('current_game')}/`);
    // initial game setup
    // set the category name
    category.innerText = response.data.category;
    // set the scores
    active_player_score.innerText = response.data.game_score;
    if (second_player_score && response.data.other_player_game_score){
        second_player_score.innerText = response.data.other_player_game_score;
    }

    // set the players names
    if(response.data.player_name){
        active_player_name.innerText = response.data.player_name;
    }
    if (response.data.other_player_name && second_player_name){
        second_player_name.innerText = response.data.other_player_name;
    }

    // add the letters
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
    if(active_player_score.innerText!== data.game_score){
        let Cont={val:active_player_score.innerText} , NewVal = data.game_score;

        gsap.to(Cont,2,{val:NewVal,roundProps:"val",onUpdate:function(){
                active_player_score.innerHTML=Cont.val
        }});
    }


    if (document.getElementById('turn')){
        if (data.status==='not your turn'){
            document.getElementsByClassName('letter-buttons')[0].classList.add('cursor-not-allowed')
            document.getElementById('turn').innerText="WAITING FOR OTHER PLAYER"
        }else{
            document.getElementsByClassName('letter-buttons')[0].classList.remove('cursor-not-allowed')
            document.getElementById('turn').innerText="";
        }
    }
    if (second_player_score){
        if(second_player_score.innerText!== data.other_player_game_score){
            let Cont={val:second_player_score.innerText} , NewVal = data.other_player_game_score;

            gsap.to(Cont,2,{val:NewVal,roundProps:"val",onUpdate:function(){
                    second_player_score.innerHTML=Cont.val
                }});
        }
    }
    // show data that constantly updates
    for (let i in data.word){
        // if the letter is different animate in the new correct letter
        if(phrase.children[i].innerText.toUpperCase()!==data.word[i].toUpperCase()){
            let tl = gsap.timeline();
            tl.to(phrase.children[i],{y:10,opacity:0, duration: 0.5});
            tl.set(phrase.children[i],{text:data.word[i],y:-10})
            tl.to(phrase.children[i],{y:0,duration:0.7,opacity:1})
        }
    }
    for(let el of document.getElementsByClassName("letter-button active")){
        if(data.correct_guesses.includes(el.innerText.toLowerCase())){
            el.classList.remove('active');
            el.classList.add("correct");
        }else if(data.incorrect_guesses.includes(el.innerText.toLowerCase())){
            el.classList.remove('active');
            el.classList.add("incorrect");
        }
    }

    if(data.status==='you won'){
        confetti()
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
    document.getElementsByClassName('letter-buttons')[0].classList.add('cursor-wait');
    e.target.classList.add('active');
    let value = e.target.innerText;
    axios.put(`/api/game/${readCookie('current_game')}/`,{guess:value}).then(response=>{
        document.getElementsByClassName('letter-buttons')[0].classList.remove('cursor-wait');
        displayGameData(response.data);
    })
}


export default function loadGamePage(){
    category = document.getElementById("category");
    loadGameData();

    phrase = document.getElementById("phrase");
    active_player_name = document.getElementById("active_player_name");
    active_player_score = document.getElementById("active_player_score");
    second_player_score = document.getElementById("second_player_score");
    second_player_name = document.getElementById("second_player_name");

    for (let item of document.getElementsByClassName('letter-button')){
        item.onclick = guessLetter;
    }
}
