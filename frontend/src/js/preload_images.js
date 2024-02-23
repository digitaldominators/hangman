import joinGameStage from "../images/join_game_stage.png";
import dd_logo from "../images/dd_logo.png";
import HangmanStage from "../images/HangmanStage.png";
import StickMan from "../images/StickMan.png";
import Stage_Retro from "../images/Stage_Retro.png";
import Stage_Creepy from "../images/Stage_Creepy.png";
import RobotBlack from "../images/RobotBlack.png";
import Noose from "../images/Noose.png";
import hangman from "../images/hangman.png";
import Dominator_Robot from "../images/Dominator_Robot.png";
import DD_LogoName from "../images/DD_LogoName.png";
import MainMenuFrame from "../images/MenuDropDown/MainMenuFrame.png";

var image_urls = [
  joinGameStage,
  dd_logo,
  HangmanStage,
  youwon,
  youlost,
  YouLose,
  StickMan,
  Stage_Retro,
  Stage_Creepy,
  RobotBlack,
  Noose,
  hangman,
  Dominator_Robot,
  DD_LogoName,
  MainMenuFrame,
];
var images = [];
function preload(images) {
  for (let i = 0; i < image_urls.length; i++) {
    images[i] = new Image();
    images[i].src = image_urls[i];
  }
  console.log(images);
}
document.addEventListener("DOMContentLoaded", function () {
  preload(images);
  console.log("preloaded images");
});
