import baseimage from '/images/HangmanStage.png';
// stick figure images
import stickHeadImage from '/images/lives/stick/stickHead.svg';
import stickTorsoImage from '/images/lives/stick/stickTorso.svg';
import stickLeftArmImage from '/images/lives/stick/stickLArm.svg';
import stickRightArmImage from '/images/lives/stick/stickRArm.svg';
import stickLeftLegImage from '/images/lives/stick/stickLLeg.svg';
import stickRightLegImage from '/images/lives/stick/stickRLeg.svg';
// skele images
import skeleHeadImage from '/images/lives/skele/skeleHead.png';
import skeleTorsoImage from '/images/lives/skele/skeleTorso.png';
import skeleLeftArmImage from '/images/lives/skele/skele_LArm.png';
import skeleRightArmImage from '/images/lives/skele/skele_RArm.png';
import skeleLeftLegImage from '/images/lives/skele/skele_LLeg.png';
import skeleRightLegImage from '/images/lives/skele/skele_RLeg.png';

// constants
const canvas = document.getElementById('myCanvas');
const slider = document.getElementById('slider');
const context = canvas.getContext('2d');
const canvasWidth = canvas.width;
const canvasHeight = canvas.height;

const bodyParts = {
    stick: [
        {name: 'head', x: 325, y: 150, width: 70, height: 70, url: stickHeadImage},
        {name: 'torso', x: 355, y: 210, width: 13, height: 100, url: stickTorsoImage},
        {name: 'left_arm', x: 290, y: 218, width: 76, height: 105, url: stickLeftArmImage},
        {name: 'right_arm', x: 350, y: 212, width: 69, height: 105, url: stickRightArmImage},
        {name: 'left_leg', x: 290, y: 300, width: 97, height: 142, url: stickLeftLegImage},
        {name: 'right_leg', x: 345, y: 290, width: 87, height: 146, url: stickRightLegImage}
    ],
    skele: [
        {name: 'head', x: 310, y: 140, width: 100, height: 100, url: skeleHeadImage},
        {name: 'torso', x: 310, y: 215, width: 100, height: 100, url: skeleTorsoImage},
        {name: 'left_arm', x: 270, y: 223, width: 76, height: 105, url: skeleLeftArmImage},
        {name: 'right_arm', x: 380, y: 223, width: 76, height: 105, url: skeleRightArmImage},
        {name: 'left_leg', x: 270, y: 310, width: 97, height: 142, url: skeleLeftLegImage},
        {name: 'right_leg', x: 335, y: 302, width: 105, height: 160, url: skeleRightLegImage}
    ]
};

let bodyType = 'skele';

let body_part_index = 0
function draw_image(url, x, y, width, height){
    let image = new Image();
    image.src = url;
    image.onload = function(){
        context.drawImage(image, x, y, width, height);
    }
}

function make_base()
{
    body_part_index = 0;
    context.clearRect(0, 0, canvas.width, canvas.height);
    draw_image(baseimage, 0, 0, canvasWidth, canvasHeight);
}
function draw_next_body_part(){
    const part = bodyParts[bodyType][body_part_index]
    draw_image(part.url, part.x, part.y, part.width, part.height)
    body_part_index += 1
}

function draw_percent_of_body(percent){
    const number_of_parts = bodyParts[bodyType].length;
    const parts_to_draw = Math.min(Math.round((percent/100) * number_of_parts),100);
    if (parts_to_draw < body_part_index){
        make_base();
    }
    for (let i = body_part_index; i < parts_to_draw; i++){
        draw_next_body_part();
    }
}

function switchBodyType(bType){
    bodyType = bType;
    make_base();
    draw_percent_of_body(slider.value)
}
make_base();
draw_percent_of_body(100);
document.getElementById('next_part').addEventListener('click', draw_next_body_part)
slider.addEventListener('change', function(){
    draw_percent_of_body(this.value)
})

for(let key in bodyParts){
    let button = document.createElement("button")
    button.innerText = key
    button.addEventListener('click', function(){
        switchBodyType(key)
    })
    document.body.appendChild(button)
}