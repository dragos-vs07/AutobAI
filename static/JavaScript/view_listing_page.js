
let prevEl = null;

const favIcon = document.getElementById("fav_icon");
if (favIcon) {
    if (Isfavourite == "True")
        favIcon.classList.add("is-favourited");
    else
        favIcon.classList.add("is-not-favourited");
}

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

function evaluate_auto(listingId)
{
    fetch(`/API/predict_price?listing_id=${listingId}`)
    .then(response => {
        if(response.ok)
        {
            response.json().then(data => {
                    if(price >= data.predicted_price)
                        document.getElementById("display_pred_box").textContent = `The car evaluated at a price of ${data.predicted_price} €, ${price-data.predicted_price} € less than the listed price of ${price} €`
                    else
                        document.getElementById("display_pred_box").textContent = `The car evaluated at a price of ${data.predicted_price} €, ${data.predicted_price-price} € more than the listed price of ${price} €`
                    document.getElementById("modal").style="display:flex;flex-direction:column;align-items: center;";
                    document.getElementById("modal_shadow").style="background: rgba(0, 0, 0, 0.7);display: flex;align-items: center;justify-content: center"

                    void document.getElementById("modal").offsetWidth;

                    requestAnimationFrame(() => {
                        document.getElementById("modal").classList.add("show");
                    });
            })
        }
    })
}
function close_modal()
{
    document.getElementById("modal").style="display:none;";
    document.getElementById("modal").classList.remove("show");
    document.getElementById("modal_shadow").style="background: rgba(0, 0, 0, 0.0);display: none;"
}
document.getElementById("modal_shadow").addEventListener("click",(e)=>{
    console.log("called");
    if(!document.getElementById("modal").contains(e.target))
        close_modal();
})
