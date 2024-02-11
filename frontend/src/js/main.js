// this file is on every page
import barba from '@barba/core';
import barbaPrefetch from '@barba/prefetch';
import {gsap} from "gsap";
import loadJoinPage from './join.js';
import loadNewPage from './new.js';
import axios from 'axios';
import readCookie from "./readCookie.js";
import loadSettingsPage from "./settings.js";
import loadChooseWordPage from "./choose_word.js";
import loadScoreBoardPage from "./scoreboard.js";
import loadInvitePage from "./invite.js";
import loadWaitPage from "./wait.js";
import loadGamePage from "./game.js";
import loadSignupPage from "./signup.js";
import loadLoginPage from "./login.js";
import './preload_images';

gsap.globalTimeline.timeScale(2);
barba.use(barbaPrefetch);


// set axios defaults
// axios.defaults.baseURL = 'http://localhost:8000';
axios.defaults.headers.post['Accept'] = 'application/json';
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.post['X-CSRFToken'] = readCookie("csrftoken");

axios.defaults.headers.put['Accept'] = 'application/json';
axios.defaults.headers.put['Content-Type'] = 'application/json';
axios.defaults.headers.put['X-CSRFToken'] = readCookie("csrftoken");


barba.init({
    // list of page transitions here
    transitions: [{
        name: 'opacity-transition',
        leave(data) {
            return gsap.to(data.current.container, {
                opacity: 0,
                display: 'none',
            });
        },
        enter(data) {
            return gsap.from(data.next.container, {
                opacity: 0
            });
        }
    }],
    // run the load code for each page.
    views: [
        {
            namespace: 'new',
            afterEnter({next}) {
                loadNewPage();
            }
        },{
            namespace: 'join',
            afterEnter({next}) {
                loadJoinPage();
            }
        },{
            namespace: 'settings',
            afterEnter({next}) {
                loadSettingsPage();
            }
        },
        {
            namespace: 'choose_word',
            afterEnter({next}) {
                loadChooseWordPage();
            }
        },
        {
            namespace: 'scoreboard',
            afterEnter({next}) {
                loadScoreBoardPage();
            }
        },
        {
            namespace: 'invite',
            afterEnter({next}) {
                loadInvitePage();
            }
        },
        {
            namespace: 'wait',
            afterEnter({next}) {
                loadWaitPage();
            }
        },
        {
            namespace: 'game',
            afterEnter(next) {
                loadGamePage();
            }
        },
        {
            namespace: 'multigame',
            afterEnter(next) {
                loadGamePage();
            }
        },
        {
            namespace: 'signup',
            afterEnter({next}) {
                loadSignupPage();
            }
        },
        {
            namespace: 'login',
            afterEnter({next}) {
                loadLoginPage();
            }
        }
    ]
});