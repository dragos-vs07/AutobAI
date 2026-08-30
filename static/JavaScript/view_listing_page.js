
let prev_el = null;

function viewImage(el)
{
    document.getElementById("view_img").src = el.src;
    if(prev_el != null)
        prev_el.style = "border: 2px,solid,white";

    el.style = "border: 2px,solid,#c9a227";
    prev_el = el;
}