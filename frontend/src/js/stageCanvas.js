import baseimage from "/images/StageNoN.png";
// stick figure images
import stickHeadImage from "/images/lives/stick/stickHead.svg";
import stickTorsoImage from "/images/lives/stick/stickTorso.png";
import stickLeftArmImage from "/images/lives/stick/stickLArm2.png";
import stickLeftHandImage from "/images/lives/stick/stickLHand.svg";
import stickRightArmImage from "/images/lives/stick/stickRArm2.svg";
import stickRightHandImage from "/images/lives/stick/stickRHand.svg";
import stickLeftLegImage from "/images/lives/stick/stickLLeg2.svg";
import stickLeftFootImage from "/images/lives/stick/stickLFoot.svg";
import stickRightLegImage from "/images/lives/stick/stickRLeg2.svg";
import stickRightFootImage from "/images/lives/stick/stickRFoot.svg";
// skele images
import skeleHeadImage from "/images/lives/skele/skeleHead.png";
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


let canvas;
let context;
let ratio;
// prettier-ignore
const bodyParts = {
  stick: [
    {name: 'noose', x: 282, y: -20, width: 160, height: 290, url: NooseImage},
    {name: 'head', x: 325, y: 150, width: 70, height: 70, url: stickHeadImage},
    {name: 'torso', x: 333, y: 200, width: 55, height: 115, url: stickTorsoImage},
    {name: 'left_arm', x: 300, y: 210, width: 75, height: 100, url: stickLeftArmImage},
    {name: 'left_hand', x: 289, y: 275, width: 50, height: 55, url: stickLeftHandImage},
    {name: 'right_arm', x: 340, y: 195, width: 75, height: 120, url: stickRightArmImage},
    {name: 'right_hand', x: 372, y: 261, width: 60, height: 75, url: stickRightHandImage},
    {name: 'left_leg', x: 295, y: 284, width: 97, height: 142, url: stickLeftLegImage},
    {name: 'left_foot', x: 270, y: 365, width: 97, height: 100, url: stickLeftFootImage},
    {name: 'right_leg', x: 340, y: 280, width: 87, height: 140, url: stickRightLegImage},
    {name: 'right_foot', x: 370, y: 340, width: 85, height: 145, url: stickRightFootImage},
    {name: 'hat', x: 315, y: 125, width: 80, height: 65, url: HatImage},
    {name: 'glasses', x: 323, y: 173, width: 80, height: 30, url: GlassesImage},
    {name: 'left_shoe', x: 280, y: 390, width: 60, height: 60, url: LeftShoeImage},
    {name: 'right_shoe', x: 382, y: 390, width: 60, height: 60, url: RightShoeImage}
  ],
  skele: [
    {name: 'noose', x: 282, y: -20, width: 160, height: 290, url: NooseImage},
    {name: "head", x: 310, y: 140, width: 100, height: 100, url: skeleHeadImage},
    {name: "torso", x: 310, y: 213, width: 100, height: 108, url: skeleTorsoImage},
    {name: "left_arm", x: 293, y: 223, width: 45, height: 98, url: skeleLeftArmImage},
    {name: 'left_hand', x: 270, y: 282, width: 55, height: 60, url: skeleLeftHandImage},
    {name: "right_arm", x: 385, y: 216, width: 50, height: 105, url: skeleRightArmImage},
    {name: 'right_hand', x: 402, y: 273, width: 60, height: 79, url: skeleRightHandImage},
    {name: "left_leg", x: 299, y: 305, width: 85, height: 135, url: skeleLeftLegImage},
    {name: 'left_foot', x: 283, y: 383, width: 82, height: 70, url: skeleLeftFootImage},
    {name: "right_leg", x: 343, y: 302, width: 70, height: 140, url: skeleRightLegImage},
    {name: 'right_foot', x: 345, y: 388, width: 80, height: 65, url: skeleRightFootImage},
    {name: 'hat', x: 315, y: 125, width: 80, height: 65, url: HatImage},
    {name: 'glasses', x: 322, y: 175, width: 80, height: 30, url: GlassesImage},
    {name: 'left_shoe', x: 289, y: 397, width: 60, height: 60, url: LeftShoeImage},
    {name: 'right_shoe', x: 365, y: 398, width: 60, height: 60, url: RightShoeImage}
  ],
};

const bodyType = "stick";

let body_part_index = 0;

export function refreshCanvas(currentpercent) {
  canvas = document.getElementById("gameStage");
  context = canvas.getContext("2d");
  canvas.style.width = "100%";
  canvas.style.height = "100%";
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  ratio = Math.min(canvas.width / 700, canvas.height / 700);
  body_part_index = 0;
  make_base();
  if (currentpercent) {
    draw_percent_of_body(currentpercent);
  }
  draw_percent_of_body(0);
}
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
export function draw_next_body_part() {
  const part = bodyParts[bodyType][body_part_index];
  draw_image(part.url, part.x, part.y, part.width, part.height);
  body_part_index += 1;
}

export function draw_percent_of_body(percent) {
  const number_of_parts = bodyParts[bodyType].length;
  const parts_to_draw = Math.min(
    Math.round((percent / 100) * number_of_parts),
    100
  );
  if (parts_to_draw < body_part_index) {
    make_base();
  }
  for (let i = body_part_index; i < parts_to_draw; i++) {
    draw_next_body_part();
  }
}
