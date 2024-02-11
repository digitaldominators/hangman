import axios from "axios";
import barba from "@barba/core";
import {setCookie} from './readCookie.js';
let form;
let username_box;
let password_box;
let error_message;
function login_user(e){
    e.preventDefault();

    // get the form's data
    const formData = new FormData(login_form);

    axios.post('/accounts/login/',{
        username:formData.get("username"),
        password:formData.get("password")
    }).then(response=>{
        error_message.innerText = "";
        setCookie('username',formData.get('username'),100);
        barba.go('/index');
    })// .catch(error=>{
        // if(error.response.data.Message){
            // error_message.innerText = error.response.data.Message
        // }
    // })
}

export default function loadLoginPage(){
    form = document.getElementById('login_form');
    username_box = document.getElementById('username_box');
    password_box = document.getElementById('password_box');
    error_message = document.getElementById('error_message');
    username_box.focus();
    form.onsubmit = login_user;
}