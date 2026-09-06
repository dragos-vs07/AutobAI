
let prev_el = null;

if (Isfavourite == "True")
    document.getElementById("fav_icon").classList.add("is-favourited");
else
    document.getElementById("fav_icon").classList.add("is-not-favourited");

function viewImage(el)
{
    document.getElementById("view_img").src = el.src;
    if(prev_el != null)
        prev_el.style = "border: 2px,solid,white";

    el.style = "border: 2px,solid,#c9a227";
    prev_el = el;
}
function checkFavourite(event)
{
    event.stopPropagation();
    const svg = event.currentTarget;

    fetch(`/API/check_favourite?listing_id=${ListingId}`)
    .then(response => response.json())
    .then(data => {
        if(data.status == "success")
        {
            console.log(data.favourited);
                if(data.favourited == "True")
                    svg.classList.replace("is-not-favourited","is-favourited");
                else
                    svg.classList.replace("is-favourited","is-not-favourited");
        }

        else
        console.log("failed_favourite");
    })
}