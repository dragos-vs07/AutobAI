
let prevEl = null;

if (Isfavourite == "True")
    document.getElementById("fav_icon").classList.add("is-favourited");
else
    document.getElementById("fav_icon").classList.add("is-not-favourited");

function viewImage(el)
{
    document.getElementById("view_img").src = el.src;
    if(prevEl != null)
        prevEl.style = "border: 2px,solid,white";

    el.style = "border: 2px,solid,#c9a227";
    prevEl = el;
}
function checkFavourite(event)
{
    event.stopPropagation();
    const svg = event.currentTarget;

    fetch(`/API/toggle_favourite?listing_id=${listingId}`)
    .then(response => {
        if(response.ok)
        {
            response.json().then(data => {
                if(data.favourited == "True")
                    svg.classList.replace("is-not-favourited","is-favourited");
                else
                    svg.classList.replace("is-favourited","is-not-favourited");
            })
        }
        else
        {
            response.json().then(data => {
            alert(`Toggle favourite failed, ${data.message}`);
            })
        }
    })
}