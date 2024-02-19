import axios from "axios";
import barba from "@barba/core";
import {setCookie} from './readCookie.js';
let form;
let username;
let password;
let error_message;
function login_user(e){
    e.preventDefault();

    // get the form's data
    const formData = new FormData(login_form);

    axios.post('/api/accounts/login_user/',{
        username:formData.get("username"),
        password:formData.get("password")
    }).then(response=>{
        error_message.innerText = "";
        barba.go('/index');
    }).catch(error=>{
        if(error.response.data.message){
            error_message.innerText = error.response.data.message
        }
    })
}

export default function loadLoginPage(){
    form = document.getElementById('login_form');
    username = document.getElementById('username_box');
    password = document.getElementById('password_box');
    error_message = document.getElementById('error_message');
    username.focus();
    form.onsubmit = login_user;
}