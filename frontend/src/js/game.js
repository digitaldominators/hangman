import moment from "moment";
import axios from "axios";
import readCookie, { setCookie } from "./readCookie.js";
import { gsap } from "gsap";
import confetti from "./confetti.js";
import {
  draw_percent_of_body,
  set_body_type,
  refreshCanvas,
} from "./stageCanvas.js";

let category;
let phrase;
let active_player_name;
let active_player_score;
let second_player_score;
let second_player_name;
let timer;
let next_turn_time = null;
let incorrect_guesses = 0;
let level;
let second_player_data_interval_id;
function draw_next_loss_percent() {
  incorrect_guesses++;
  let percent = 0;
  if (level === 1) {
    percent = 100 / 18;
  } else if (level === 2) {
    percent = 100 / 10;
  } else if (level === 3) {
    percent = 100 / 6;
  }
  draw_percent_of_body(percent * incorrect_guesses);
}

function set_turn_time() {
  if (next_turn_time) {
    timer.classList.remove("opacity-0");
    const next_time = moment(next_turn_time);
    const duration = moment.duration(next_time.diff(moment()));
    if (duration > 0) {
      if (duration.seconds() > 10) {
        timer.innerText = duration.minutes() + ":" + duration.seconds();
      } else {
        timer.innerText = duration.minutes() + ":0" + duration.seconds();
      }
    } else {
      timer.innerText = "0:00";
    }
  } else {
    timer?.classList.add("opacity-0");
  }
}

async function loadGameData() {
  let response = await axios.get(`/api/game/${readCookie("current_game")}/`);
  // initial game setup
  // set the category name
  category.innerText = response.data.category;
  level = response.data.level;
  // set the scores
  active_player_score.innerText = response.data.game_score;
  if (second_player_score && response.data.other_player_game_score) {
    second_player_score.innerText = response.data.other_player_game_score;
  }

  // set the players names
  if (response.data.player_name) {
    active_player_name.innerText = response.data.player_name;
  } else {
    let p = document.createElement("p");
    p.innerHTML = `<a href="/login" style="color: blue">Login</a> to save your scores`;
    document.getElementById("game_over_message_box").appendChild(p);
  }
  if (response.data.other_player_name && second_player_name) {
    second_player_name.innerText = response.data.other_player_name;
  }

  // set the timer
  next_turn_time = response.data.next_turn_time;

  // add the letters
  let letters = "";
  for (let letter of response.data.word) {
    letters += `<li class="letter guessed">${letter}</li>`;
  }

  //set state of letters that were pressed before reload (if correct or incorrect letters
  for (const letter of document.getElementsByClassName("letter-button")) {
    if (
      response.data.correct_guesses.includes(letter.innerText.toLowerCase())
    ) {
      letter.classList.add("correct");
    } else if (
      response.data.incorrect_guesses.includes(letter.innerText.toLowerCase())
    ) {
      letter.classList.add("incorrect");
    }
  }
  for (let i in response.data.incorrect_guesses) {
    draw_next_loss_percent();
  }
  phrase.innerHTML = letters;

  if (response.data.is_multiplayer) {
    second_player_data_interval_id = setTimeout(() => {
      getSecondPlayerData();
    }, 1000);
  }

  if (response.data.status === "you won") {
    winGame();
  }

  if (response.data.status === "you lost") {
    loseGame();
  }
}

function getSecondPlayerData() {
  if (readCookie("current_game") === null) {
    return;
  }
  axios
    .get(`/api/game/${readCookie("current_game")}/`)
    .then((response) => {
      displayGameData(response.data);
      if (
        response.data.status === "you won" ||
        response.data.status === "you lost"
      ) {
        return;
      }
      setTimeout(() => {
        getSecondPlayerData();
      }, 1000);
    })
    .catch(() => {
      setTimeout(() => {
        getSecondPlayerData();
      }, 1000);
    });
}
function displayGameData(data) {
  if (active_player_score.innerText !== data.game_score) {
    let Cont = { val: active_player_score.innerText },
      NewVal = data.game_score;

    gsap.to(Cont, 2, {
      val: NewVal,
      roundProps: "val",
      onUpdate: function () {
        active_player_score.innerHTML = Cont.val;
      },
    });
  }

  // set the timer
  next_turn_time = data.next_turn_time;

  if (document.getElementById("turn")) {
    if (data.status === "not your turn") {
      document
        .getElementsByClassName("letter-buttons")[0]
        .classList.add("cursor-not-allowed");
      if (data.other_player_name) {
        document.getElementById(
          "turn"
        ).innerText = `${data.other_player_name}'s Turn`;
      } else {
        document.getElementById("turn").innerText = "Other Player's Turn";
      }
    } else {
      document
        .getElementsByClassName("letter-buttons")[0]
        .classList.remove("cursor-not-allowed");
      document.getElementById("turn").innerText = "Your Turn";
    }
  }

  if (second_player_score) {
    if (second_player_score.innerText !== data.other_player_game_score) {
      let Cont = { val: second_player_score.innerText },
        NewVal = data.other_player_game_score;

      gsap.to(Cont, 2, {
        val: NewVal,
        roundProps: "val",
        onUpdate: function () {
          second_player_score.innerHTML = Cont.val;
        },
      });
    }
  }
  // show letters
  for (let i in data.word) {
    /*
            [...data.word][i].toUpperCase()
            this converts a string to a list of characters so that the emoji characters indexed returns the emoji and not its character code
            i.e. a = '🌕'; a[0] -> '\uD83C';
            this converts it to a = ['🌕']; a[0] -> '🌕';
            Which allows emojis to be matched correctly and not be replaced with �
        */
    // if the letter is different animate in the new correct letter
    if (
      phrase.children[i].innerText.toUpperCase() !==
      [...data.word][i].toUpperCase()
    ) {
      let tl = gsap.timeline();
      tl.to(phrase.children[i], { y: 10, opacity: 0, duration: 0.5 });
      tl.set(phrase.children[i], { text: data.word[i], y: -10 });
      tl.to(phrase.children[i], { y: 0, duration: 0.7, opacity: 1 });
    }
  }

  // make letters red or green if letters were already chosen
  for (let el of document.getElementsByClassName("letter-button active")) {
    if (data.correct_guesses.includes(el.innerText.toLowerCase())) {
      el.classList.remove("active");
      el.classList.add("correct");
    } else if (data.incorrect_guesses.includes(el.innerText.toLowerCase())) {
      el.classList.remove("active");
      el.classList.add("incorrect");
      draw_next_loss_percent();
    }
  }

  if (data.status === "you won") {
    winGame();
  }

  if (data.status === "you lost") {
    loseGame();
  }
}

function gameEnded() {
  // stop trying to fetch the other players scores the game is over
  if (second_player_data_interval_id) {
    clearInterval(second_player_data_interval_id);
  }
  // set the current game cookie to expire
  // so that the player has to choose a different game
  setCookie("current_game", "", -1);
}

function winGame() {
  confetti();
  const timeline = gsap.timeline();
  document.getElementsByClassName("game-container")[0].classList.add("over");
  const dialog = document.querySelector("#game_over_message_box");
  dialog.showModal();
  draw_percent_of_body(0);
  timeline.to(
    document.getElementById("gameStageContainer"),
    { duration: 1, y: 100, scale: 0.9 },
    "anim_start"
  );
  timeline.to(document.getElementById("game_over_message"), {
    duration: 3,
    text: "You Won!",
    ease: "power2.out",
  });
  timeline.to(
    document.getElementById("game_over_message_box"),
    { duration: 4, borderColor: "rgb(2,65,2)" },
    "anim_start"
  );

  gameEnded();
}

function loseGame() {
  const timeline = gsap.timeline();
  document.getElementsByClassName("game-container")[0].classList.add("over");
  const dialog = document.querySelector("#game_over_message_box");
  dialog.showModal();
  draw_percent_of_body(100);
  timeline.to(
    document.getElementById("gameStageContainer"),
    { duration: 1, y: 100, scale: 1.3 },
    "anim_start"
  );
  timeline.to(document.getElementById("game_over_message"), {
    duration: 3,
    text: "You Lost :(",
    ease: "power2.out",
  });
  timeline.to(
    document.getElementById("game_over_message_box"),
    { duration: 4, borderColor: "rgb(255,0,0)" },
    "anim_start"
  );

  gameEnded();
}

function guessLetter(e) {
  document
    .getElementsByClassName("letter-buttons")[0]
    .classList.add("cursor-wait");
  e.target.classList.add("active");
  let value = e.target.innerText;
  axios
    .put(`/api/game/${readCookie("current_game")}/`, { guess: value })
    .then((response) => {
      document
        .getElementsByClassName("letter-buttons")[0]
        .classList.remove("cursor-wait");
      displayGameData(response.data);
    });
}

function guessWord(e) {
  e.preventDefault();
  const word_guess_input = document.getElementById("word_guess_input");

  let value = word_guess_input.value;

  axios
    .put(`/api/game/${readCookie("current_game")}/`, { guess: value })
    .then((response) => {
      document
        .getElementsByClassName("letter-buttons")[0]
        .classList.remove("cursor-wait");
      displayGameData(response.data);
      word_guess_input.value = "";
      if (incorrect_guesses < response.data.incorrect_guesses.length) {
        draw_next_loss_percent();
      }
    });
  document.getElementById("word_guess_box").close();
}

export default function loadGamePage() {
  incorrect_guesses = 0;
  category = document.getElementById("category");
  timer = document.getElementById("timer");
  if (readCookie("character") === "skele") {
    set_body_type("skele");
  } else {
    set_body_type("stick");
  }

  loadGameData();

  phrase = document.getElementById("phrase");
  active_player_name = document.getElementById("active_player_name");
  active_player_score = document.getElementById("active_player_score");
  second_player_score = document.getElementById("second_player_score");
  second_player_name = document.getElementById("second_player_name");

  phrase = document.getElementById("phrase");
  active_player_name = document.getElementById("active_player_name");
  active_player_score = document.getElementById("active_player_score");
  second_player_score = document.getElementById("second_player_score");
  second_player_name = document.getElementById("second_player_name");

  for (let item of document.getElementsByClassName("letter-button")) {
    item.onclick = guessLetter;
  }

  document.getElementById("guessButton").onclick = () => {
    document.getElementById("word_guess_box").showModal();
  };
  document.getElementById("guess_word_form").onsubmit = guessWord;
  refreshCanvas(0);
  setInterval(set_turn_time, 500);

  document
    .getElementById("sound-button")
    .addEventListener("click", function () {
      if (document.getElementById("game_music").paused) {
        document.getElementById("game_music").play();
      } else {
        document.getElementById("game_music").pause();
      }
    });
}
