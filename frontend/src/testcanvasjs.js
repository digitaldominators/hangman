import baseimage from "/images/StageNoN.png";
// stick figure images
import stickHeadImage from "/images/lives/stick/stickHead2.png";
import stickRightEyeImage from "/images/lives/stick/stickREye.png";
import stickLeftEyeImage from "/images/lives/stick/stickLEye.png";
import stickMouthImage from "/images/lives/stick/stickMouth.png";
import stickTorsoImage from "/images/lives/stick/stickTorso2.png";
import stickLeftArmImage from "/images/lives/stick/stickLArm2.png";
import stickLeftHandImage from "/images/lives/stick/stickLHand.svg";
import stickRightArmImage from "/images/lives/stick/stickRArm2.svg";
import stickRightHandImage from "/images/lives/stick/stickRHand.svg";
import stickLeftLegImage from "/images/lives/stick/stickLLeg2.svg";
import stickLeftFootImage from "/images/lives/stick/stickLFoot.svg";
import stickRightLegImage from "/images/lives/stick/stickRLeg2.svg";
import stickRightFootImage from "/images/lives/stick/stickRFoot.svg";
// skele images
import skeleHeadImage from "/images/lives/skele/skeleHead2.png";
import skeleRightEyeImage from "/images/lives/skele/skeleREye.png";
import skeleLeftEyeImage from "/images/lives/skele/skeleLEye.png";
import skeleNoseImage from "/images/lives/skele/skeleNose.png";
import skeleTorsoImage from "/images/lives/skele/skeleTorso.svg";
import skeleLeftArmImage from "/images/lives/skele/skeleLArm.svg";
import skeleLeftHandImage from "/images/lives/skele/skeleLHand.svg";
import skeleRightArmImage from "/images/lives/skele/skeleRArm.svg";
import skeleRightHandImage from "/images/lives/skele/skeleRHand.svg";
import skeleLeftLegImage from "/images/lives/skele/skeleLLeg.svg";
import skeleLeftFootImage from "/images/lives/skele/skeleLFoot.svg";
import skeleRightLegImage from "/images/lives/skele/skeleRLeg.svg";
import skeleRightFootImage from "/images/lives/skele/skeleRFoot.svg";
// items
import GlassesImage from "/images/lives/items/glasses.svg";
import HatImage from "/images/lives/items/hat.svg";
import LeftShoeImage from "/images/lives/items/LShoe.svg";
import RightShoeImage from "/images/lives/items/RShoe.svg";
import NooseImage from "/images/lives/items/noose.svg";

// constants
const canvas = document.getElementById("myCanvas");
const slider = document.getElementById("slider");
const context = canvas.getContext("2d");

// prettier-ignore
const bodyParts = {
  stick: [
	{name: 'noose', x: 282, y: -20, width: 160, height: 290, url: NooseImage},
    	{name: 'head', x: 295, y: 112, width: 130, height: 165, url: stickHeadImage},
	{name: 'right_eye', x: 349, y: 158, width: 50, height: 50, url: stickRightEyeImage},
	{name: 'left_eye', x: 318, y: 158, width: 50, height: 50, url: stickLeftEyeImage},
	{name: 'mouth', x: 336, y: 181, width: 50, height: 40, url: stickMouthImage},
    	{name: 'torso', x: 333, y: 205, width: 55, height: 110, url: stickTorsoImage},
    	{name: 'left_arm', x: 300, y: 212, width: 75, height: 100, url: stickLeftArmImage},
	{name: 'left_hand', x: 289, y: 275, width: 50, height: 55, url: stickLeftHandImage},
    	{name: 'right_arm', x: 340, y: 199, width: 75, height: 120, url: stickRightArmImage},
	{name: 'right_hand', x: 370, y: 261, width: 60, height: 75, url: stickRightHandImage},
    	{name: 'left_leg', x: 295, y: 289, width: 97, height: 130, url: stickLeftLegImage},
	{name: 'left_foot', x: 272, y: 365, width: 92, height: 95, url: stickLeftFootImage},
    	{name: 'right_leg', x: 338, y: 280, width: 87, height: 140, url: stickRightLegImage},
	{name: 'right_foot', x: 367, y: 340, width: 85, height: 138, url: stickRightFootImage},
	{name: 'hat', x: 308, y: 110, width: 100, height: 80, url: HatImage},
	{name: 'glasses', x: 321, y: 173, width: 80, height: 30, url: GlassesImage},
	{name: 'left_shoe', x: 280, y: 390, width: 60, height: 60, url: LeftShoeImage},
	{name: 'right_shoe', x: 384, y: 390, width: 60, height: 60, url: RightShoeImage}
  ],
  skele: [
	{name: 'noose', x: 282, y: -20, width: 160, height: 290, url: NooseImage},
    	{name: "head", x: 300, y: 120, width: 120, height: 120, url: skeleHeadImage},
	{name: 'right_eye', x: 365, y: 165, width: 25, height: 37, url: skeleRightEyeImage},
	{name: 'left_eye', x: 335, y: 165, width: 25, height: 37, url: skeleLeftEyeImage},
	{name: 'nose', x: 351, y: 183, width: 22, height: 22, url: skeleNoseImage},
    	{name: "torso", x: 315, y: 213, width: 90, height: 115, url: skeleTorsoImage},
    	{name: "left_arm", x: 293, y: 226, width: 44, height: 98, url: skeleLeftArmImage},
	{name: 'left_hand', x: 270, y: 282, width: 55, height: 60, url: skeleLeftHandImage},
    	{name: "right_arm", x: 385, y: 220, width: 45, height: 105, url: skeleRightArmImage},
	{name: 'right_hand', x: 398, y: 275, width: 60, height: 79, url: skeleRightHandImage},
    	{name: "left_leg", x: 301, y: 314, width: 85, height: 135, url: skeleLeftLegImage},
	{name: 'left_foot', x: 283, y: 393, width: 82, height: 70, url: skeleLeftFootImage},
    	{name: "right_leg", x: 342, y: 312, width: 70, height: 140, url: skeleRightLegImage},
	{name: 'right_foot', x: 345, y: 397, width: 82, height: 65, url: skeleRightFootImage},
	{name: 'hat', x: 309, y: 105, width: 100, height: 85, url: HatImage},
	{name: 'glasses', x: 322, y: 175, width: 80, height: 30, url: GlassesImage},
	{name: 'left_shoe', x: 296, y: 397, width: 60, height: 60, url: LeftShoeImage},
	{name: 'right_shoe', x: 363, y: 398, width: 60, height: 60, url: RightShoeImage}
  ],
};

let bodyType = "skele";

let body_part_index = 0;

const ratio = Math.min(canvas.width / 700, canvas.height / 700);
function draw_image(url, x, y, width, height) {
  let image = new Image();
  image.src = url;
  image.onload = function () {
    context.drawImage(
      image,
      x * ratio,
      y * ratio,
      width * ratio,
      height * ratio
    );
  };
}

function make_base() {
  body_part_index = 0;
  context.clearRect(0, 0, canvas.width, canvas.height);
  draw_image(baseimage, 0, 0, 700, 700);
}
function draw_next_body_part() {
  const part = bodyParts[bodyType][body_part_index];
  draw_image(part.url, part.x, part.y, part.width, part.height);
  body_part_index += 1;
}

function draw_percent_of_body(percent) {
  const number_of_parts = bodyParts[bodyType].length;
  const parts_to_draw = Math.min(
    Math.round((percent / 100) * number_of_parts),
    100
  );
  if (parts_to_draw <= body_part_index) {
    make_base();
  }
  for (let i = body_part_index; i < parts_to_draw; i++) {
    draw_next_body_part();
  }
}

function switchBodyType(bType) {
  bodyType = bType;
  make_base();
  draw_percent_of_body(slider.value);
}
make_base();
draw_percent_of_body(100);
document
  .getElementById("next_part")
  .addEventListener("click", draw_next_body_part);
slider.addEventListener("change", function () {
  draw_percent_of_body(this.value);
});

for (let key in bodyParts) {
  let button = document.createElement("button");
  button.innerText = key;
  button.addEventListener("click", function () {
    switchBodyType(key);
  });
  document.body.appendChild(button);
}
