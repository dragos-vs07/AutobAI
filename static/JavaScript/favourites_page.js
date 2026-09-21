const LPP = 5;
let currentPage = 1;
let currentTotal = 0;

function updateButtons()
{
    const totalPages = Math.max(1, Math.ceil(currentTotal / LPP));
    document.getElementById("previous_page_btn").classList.toggle("hide_button", currentPage <= 1);
    document.getElementById("next_page_btn").classList.toggle("hide_button", currentPage >= totalPages);
    document.getElementById("current_page").textContent = currentPage;
}

function getAndDisplayListings()
{
    
    fetch(`/API/get_listings?page=${currentPage}&lpp=${LPP}&favourites=True`)
    .then( response => response.json())
    .then(data => {

        const container = document.getElementById("listings_area");
        container.innerHTML = "";
        currentTotal = data.total;
        updateButtons();

        for (const listing of data.listings )
            {

                const cell = document.createElement("div");
                cell.classList.add("listing");

                const coverImg = document.createElement("img");

                coverImg.src = listing.cover_img_path;
                coverImg.classList.add("image");

                const title = document.createElement("h4");

                title.textContent = listing.title;

                const price = document.createElement("h4");
                price.textContent = listing.price + " €";

                const carDef = document.createElement("div");
                carDef.style = "display:flex; flex-direction:row; gap: 5px;"

                const brand = document.createElement("p");
                brand.textContent = listing.brand;

                carDef.appendChild(brand)

                const model = document.createElement("p");
                model.textContent = listing.model;

                carDef.appendChild(model)

                const mileage = document.createElement("p");
                mileage.textContent = `${listing.mileage} km`;

                cell.appendChild(title);
                cell.appendChild(coverImg);
                cell.appendChild(price);
                cell.appendChild(carDef);
                cell.appendChild(mileage);
                cell.appendChild(document.createElement("br"));
                cell.addEventListener('click',()=>{
                    window.location.href = `/viewlisting?listing_id=${listing.listing_id}`;
                })
                container.appendChild(cell);
            }
        if(data.listings.length == 0)
        {
                const message = document.createElement("p");
                message.style = "color: white; text-align: center; font-size: large;"
                message.innerText = "You marked no listings as favourites";
                document.getElementById("listings_area").appendChild(message);
        } 
    })
}
function nextpage()
{
    const totalPages = Math.max(1, Math.ceil(currentTotal / LPP));
    if (currentPage >= totalPages) return;
    currentPage = currentPage + 1;
    getAndDisplayListings();
    window.scrollTo(0, 0);
}

function previouspage()
{
    if(currentPage == 1 ) return;

    currentPage = Math.max(1,currentPage - 1);
    getAndDisplayListings();
    window.scrollTo(0, 0);
}

getAndDisplayListings();