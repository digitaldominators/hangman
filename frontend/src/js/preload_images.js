var image_urls = [
    "/images/join_game_stage.png",
    "/images/dd_logo.png",
    "/images/HangmanStage.png",
    "/images/youwon.png",
    "/images/youlost.png",
    "/images/YouLose.PNG",
    "/images/StickMan.png",
    "/images/Stage_Retro.PNG",
    "/images/Stage_Creepy.PNG",
    "/images/RobotBlack.PNG",
    "/images/Noose.PNG",
    "/images/hangman.png",
    "/images/Dominator_Robot.png",
    "/images/DD_LogoName.png",
    "/images/dd_logo.png",
    "/images/dd_logo.jpg",
    "/images/MenuDropDown/MainMenuFrame.png"
];
var images = [];
function preload(images) {
    for (let i = 0; i < image_urls.length; i++) {
        images[i] = new Image()
        images[i].src = image_urls[i];
    }
    console.log(images)
}
document.addEventListener("DOMContentLoaded", function(){
    preload(
        images
    )
    console.log("preloaded images")
});
