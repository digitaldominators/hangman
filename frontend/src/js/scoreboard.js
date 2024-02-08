import axios from "axios";
let total_scores= [];
let average_scores = [];
let scoreboard_body;
let sortby = 'total_scores';
let avg_score_sort;
let total_score_sort;
async function loadScores(){
    const response = await axios.get('/api/scoreboard/');
    total_scores = response.data.total_scores;
    average_scores = response.data.average_scores;
    show_scores();
}

function show_scores(){
    if (sortby==='total_scores'){
        sortScores(total_scores)
        total_score_sort.classList.add("bold");
        avg_score_sort.classList.remove("bold");
    }else{
        sortScores(average_scores)
        avg_score_sort.classList.add("bold");
        total_score_sort.classList.remove("bold");
    }
}

function sort_average(){
    sortby = 'avg_scores';
    show_scores();
}

function sort_total(){
    sortby = 'total_scores';
    show_scores();
}
function sortScores(scores){
    let body = ""

    for(let score of scores){
        body += `
            <div class="border-2 border-black bg-white p-2 mb-1 grid grid-cols-4 gap-4">
                <div><p class="mr-2 scoreboard_text">${score.user}</p></div>
                <div></div>
                <div><p class="mr-2 scoreboard_text">${score.total_score}</p></div>
                <div><p class="scoreboard_text">${score.avg_score}</p></div></div>`
    }

    scoreboard_body.innerHTML = body;
}
export default function loadScoreBoardPage(){
    scoreboard_body = document.getElementById('scoreboard_body');
    avg_score_sort = document.getElementById("avg_score_sort");
    total_score_sort = document.getElementById("total_score_sort");

    avg_score_sort.onclick = sort_average;
    total_score_sort.onclick = sort_total;
    loadScores();
}