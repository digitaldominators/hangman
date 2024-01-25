// this file is on every page
import barba from '@barba/core';
import barbaPrefetch from '@barba/prefetch';
import {gsap} from "gsap";
import loadJoinPage from './join.js';
import loadNewPage from './new.js';
import axios from 'axios';
import readCookie from "./readCookie.js";
import loadWaitingPage from "./waiting.js";
import loadSettingsPage from "./settings.js";

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
            namespace: 'waiting',
            afterEnter({next}) {
                loadWaitingPage();
            }
        },{
            namespace: 'settings',
            afterEnter({next}) {
                loadSettingsPage();
            }
        }

    ]
});