// this file is on every page
import barba from "@barba/core";
import barbaPrefetch from "@barba/prefetch";
import { gsap } from "gsap";
import { TextPlugin } from "gsap/TextPlugin";
import loadJoinPage from "./join.js";
import loadNewPage from "./new.js";
import axios from "axios";
import readCookie from "./readCookie.js";
import loadSettingsPage from "./settings.js";
import loadChooseWordPage from "./choose_word.js";
import loadScoreBoardPage from "./scoreboard.js";
import loadInvitePage from "./invite.js";
import loadWaitPage from "./wait.js";
import loadGamePage from "./game.js";
import loadSignupPage from "./signup.js";
import loadLoginPage from "./login.js";
import loadAccountPage from "./account.js";
// import './preload_images';
gsap.registerPlugin(TextPlugin);
gsap.globalTimeline.timeScale(2);
barba.use(barbaPrefetch);

// set axios defaults
// axios.defaults.baseURL = 'http://localhost:8000';
axios.defaults.headers.post["Accept"] = "application/json";
axios.defaults.headers.post["Content-Type"] = "application/json";
axios.defaults.headers.post["X-CSRFToken"] = readCookie("csrftoken");

axios.defaults.headers.put["Accept"] = "application/json";
axios.defaults.headers.put["Content-Type"] = "application/json";
axios.defaults.headers.put["X-CSRFToken"] = readCookie("csrftoken");

barba.init({
  // list of page transitions here
  transitions: [
    {
      name: "opacity-transition",
      leave(data) {
        return gsap.to(data.current.container, {
          opacity: 0,
          display: "none",
        });
      },
      enter(data) {
        return gsap.from(data.next.container, {
          opacity: 0,
        });
      },
    },
  ],
  // run the load code for each page.
  views: [
    {
      namespace: "youlose",
      afterEnter({ next }) {
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "youwon",
      afterEnter({ next }) {
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "index",
      afterEnter({ next }) {
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "new",
      afterEnter({ next }) {
        loadNewPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "join",
      afterEnter({ next }) {
        loadJoinPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "settings",
      afterEnter({ next }) {
        loadSettingsPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "choose_word",
      afterEnter({ next }) {
        loadChooseWordPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "scoreboard",
      afterEnter({ next }) {
        loadScoreBoardPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "invite",
      afterEnter({ next }) {
        loadInvitePage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "wait",
      afterEnter({ next }) {
        loadWaitPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "game",
      afterEnter(next) {
        loadGamePage();
        document
          .getElementById("main-container")
          .classList.add("wide-container");
      },
    },
    {
      namespace: "multigame",
      afterEnter(next) {
        loadGamePage();
        document
          .getElementById("main-container")
          .classList.add("wide-container");
      },
    },
    {
      namespace: "signup",
      afterEnter({ next }) {
        loadSignupPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "login",
      afterEnter({ next }) {
        loadLoginPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
    {
      namespace: "account",
      afterEnter({ next }) {
        loadAccountPage();
        document
          .getElementById("main-container")
          .classList.remove("wide-container");
      },
    },
  ],
});
