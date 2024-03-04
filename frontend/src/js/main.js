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
import loadIndexPage from "./index.js";
import Toastify from "toastify-js";
gsap.registerPlugin(TextPlugin);
gsap.globalTimeline.timeScale(2);
barba.use(barbaPrefetch);

// set axios defaults
axios.defaults.headers.post["Accept"] = "application/json";
axios.defaults.headers.post["Content-Type"] = "application/json";

axios.defaults.headers.put["Accept"] = "application/json";
axios.defaults.headers.put["Content-Type"] = "application/json";

axios.interceptors.request.use(function (config) {
  config.headers["X-CSRFToken"] = readCookie("csrftoken");
  return config;
});

axios.interceptors.response.use(
  function (response) {
    // Optional: Do something with response data
    if (response.data?.message) {
      Toastify({
        text: response.data.message,
        backgroundColor: "green",
      }).showToast();
    }
    return response;
  },
  function (error) {
    console.log(error);
    // Do whatever you want with the response error here:
    if (error.response?.data?.message) {
      Toastify({
        text: error.response.data.message,
        backgroundColor: "red",
      }).showToast();
    } else if (error.response?.data?.non_field_errors) {
      for (let message of error.response.data.non_field_errors) {
        Toastify({
          text: message,
          backgroundColor: "red",
        }).showToast();
      }
    } else if (error.response?.data?.error) {
      for (let message of error.response.data.error) {
        Toastify({
          text: message,
          backgroundColor: "red",
        }).showToast();
      }
    } else if (error.response?.data?.detail) {
      Toastify({
        text: error.response.data.detail,
        backgroundColor: "red",
      }).showToast();
    } else if (error.response.status === 400) {
      // console.log(error.response?.data.keys())
      for (let message in error.response?.data) {
        Toastify({
          text: message + " " + error.response?.data[message],
          backgroundColor: "red",
        }).showToast();
      }
    } else {
      Toastify({
        text: "An error occurred. Reload the page and try again.",
        backgroundColor: "red",
      }).showToast();
    }

    // But, be SURE to return the rejected promise, so the caller still has
    // the option of additional specialized handling at the call-site:
    return Promise.reject(error);
  }
);

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
      namespace: "index",
      afterEnter({ next }) {
        loadIndexPage();
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
        if (readCookie("current_game") === null) {
          barba.go("/");
        } else {
          axios
            .get(`/api/game/${readCookie("current_game")}/`)
            .then((response) => {
              if (response.data.is_multiplayer) {
                barba.go("/multigame");
              }
            });
        }
        loadGamePage();
        document
          .getElementById("main-container")
          .classList.add("wide-container");
      },
    },
    {
      namespace: "multigame",
      afterEnter(next) {
        if (readCookie("current_game") === null) {
          barba.go("/");
        } else {
          axios
            .get(`/api/game/${readCookie("current_game")}/`)
            .then((response) => {
              if (!response.data.is_multiplayer) {
                barba.go("/game");
              }
            });
        }
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
