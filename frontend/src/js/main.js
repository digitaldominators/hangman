// this file is on every page
import barba from '@barba/core';
import barbaPrefetch from '@barba/prefetch';
import {gsap} from "gsap";

gsap.globalTimeline.timeScale(2);
barba.use(barbaPrefetch);

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
    }]
});