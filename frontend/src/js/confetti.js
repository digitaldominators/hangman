import {gsap,Linear,Sine} from "gsap";
// https://codepen.io/ProjectDCL/pen/ZEmKyPq
const tl = gsap.timeline();
const confetti_duration = 7000; // milliseconds
export default function confetti() {
    tl.play()
    let confettiContainer = document.getElementsByTagName("html")[0];
    let total = 100;
    let w = confettiContainer.getBoundingClientRect().width;
    let h = confettiContainer.getBoundingClientRect().height-20;

    for (let i=0; i<total; i++){
        let dot = document.createElement('div');
        dot.classList.add('confetti-dot');
        confettiContainer.append(dot)
        tl.set(document.getElementsByClassName("confetti-dot")[i],{
            x:Random(w),
            top:0,
            opacity:1,
            scale:Random(1)+1,
            backgroundColor:"hsl(" + random(170,360) + ",50%,50%)"
        },"dots");
        animm(document.getElementsByClassName("confetti-dot")[i]);
    }

    function animm(elm){
        tl
            .set(confettiContainer, {
                display: 'block'
            })
        tl.to(confettiContainer, {
            autoAlpha: 1,
            duration: 2,
            delay: 1
        })
        tl.to(elm,Random(5)+4,{
            y:h,
            ease:Linear.easeNone,
            repeat:-1,
            delay:-5
        });
        tl.to(elm,Random(5)+1,{
            x:'+=70',
            repeat:-1,
            yoyo:true,
            ease:Sine.easeInOut
        })
        tl.to(elm,Random(5)+1,{
            scaleX:0.2,
            rotation:Random(360),
            repeat:-1,
            yoyo:true,
            ease:Sine.easeInOut
        })
        tl.to(elm,Random(1)+0.5,{
            opacity:0,
            repeat:-1,
            yoyo:true,
            ease:Sine.easeInOut
        })
    }
    setTimeout(()=>{
        tl.to(".confetti-dot",{opacity:0,ease:Sine.easeInOut,duration:1})
        tl.pause()
        const elements = document.getElementsByClassName("confetti-dot");

        while (elements.length > 0) elements[0].remove();
    },confetti_duration)

    function Random (max) {
        return Math.random()*max;
    }

    function random(min, max) {
        return min + Math.floor( Math.random() * (max - min));
    }
}