import axios from "axios";
import barba from "@barba/core";
import {setCookie} from './readCookie.js';
let form;
let username;
let email;
let password;
let password2;
let error_message;
function sign_up_user(e){
    e.preventDefault();

    // get the form's data
    const formData = new FormData(sign_up_form);

    axios.post('/accounts/register/',{
        username:formData.get("username"),
        email:formData.get("email"),
        password:formData.get("password"),
        password2:formData.get("password2")
    }).then(response=>{
        error_message.innerText = '';
        setCookie('username',formData.get('username'),100);
        barba.go('/index');
    })// .catch(error=>{
        // if(error.response.data.Message){
            // error_message.innerText = error.response.data.Message
        // }
    // })
}

export default function loadSignupPage(){
    form = document.getElementById('sign_up_form');
    username = document.getElementById('username_box');
    email = document.getElementById('email_box');
    password = document.getElementById('password_box');
    password2 = document.getElementById('password2_box');
    error_message = document.getElementById('error_message');
    username.focus();
    form.onsubmit = sign_up_user;
}