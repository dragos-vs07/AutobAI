
fetch("/API/get_listings?page=1&lpp=24")
.then( response => response.json())
.then(data => {
    const container = document.getElementById("listings_area");
    container.innerHTML = "";

    for (const listing of data)
        {

            const cell = document.createElement("div");
            cell.classList.add("listing");

            const cover_img = document.createElement("img");

            cover_img.src = listing.cover_img_path;
            cover_img.style = "width: 15vw; height: 15vw"
            
            const title = document.createElement("h4");

            title.textContent = listing.title;

            const price = document.createElement("h4");
            price.textContent = listing.price + " €";

            const car_def = document.createElement("div");
            car_def.style = "display:flex; flex-direction:row; gap: 5px;"

            const brand = document.createElement("p");
            brand.textContent = listing.brand;

            car_def.appendChild(brand)

            const model = document.createElement("p");
            model.textContent = listing.model;

            car_def.appendChild(model)

            const mileage = document.createElement("p");
            mileage.textContent = `${listing.mileage} km`;

            cell.appendChild(title);
            cell.appendChild(cover_img);
            cell.appendChild(price);
            cell.appendChild(car_def);
            cell.appendChild(mileage);

            if(userId != null && userId != listing.seller_id)
            {
                
                const fav_icon = document.createElement("div");
                fav_icon.innerHTML = `<svg onclick = "checkFavourite(event)" data-listing-id = "${listing.listing_id}" xmlns="http://www.w3.org/2000/svg" class = "pic" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" >
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                        </svg>`;
                fav_icon.classList.add("fav_icon");

                if (listing.is_favourite == "True") 
                 fav_icon.querySelector("svg").classList.add("is-favourited");
                else
                fav_icon.querySelector("svg").classList.add("is-not-favourited");

                cell.appendChild(fav_icon);
            }

            
            cell.appendChild(document.createElement("br"));
            cell.addEventListener('click',()=>{
                window.location.href = `/viewlisting?listing_id=${listing.listing_id}`;
            })
            container.appendChild(cell);
        } 
})
function checkFavourite(event)
{
    event.stopPropagation();
    const svg = event.currentTarget;
    const listingId = svg.dataset.listingId;

    fetch(`/API/check_favourite?listing_id=${listingId}`)
    .then(response => response.json())
    .then(data => {
        if(data.status == "success")
        {
                if(data.favourited == "True")
                    svg.classList.replace("is-not-favourited","is-favourited");
                else
                    svg.classList.replace("is-favourited","is-not-favourited");
        }

        else
        console.log("failed_favourite");
    })
}