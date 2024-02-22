import {get_body_types,set_body_type,get_current_part_index,get_total_parts, draw_next_body_part, refreshCanvas} from "./stageCanvas.js";
let body_type_index = 0;
function next_part() {
    if(get_current_part_index() >= get_total_parts()){
        body_type_index += 1;
        set_body_type(get_body_types()[body_type_index%get_body_types().length])
        refreshCanvas();
    }

    draw_next_body_part()
    if(window.location.pathname === '/index.html' || window.location.pathname === '/'){
        setTimeout(() => {
            next_part();
        }, 700);
    }
}
export default function loadIndexPage() {
    refreshCanvas()

    setTimeout(() => {
        next_part();
    }, 500);
}