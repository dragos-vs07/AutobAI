
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

    fetch(`/API/get_listings?page=${currentPage}&seller_id=${userId}&lpp=${LPP}`)
    .then( response => response.json())
    .then( data => {

        currentTotal = data.total;
        updateButtons();

        for (const l of data.listings )
        {
            const listing = document.createElement("div");
            listing.classList.add("listing");

            const img = document.createElement("img");
            img.classList.add("image");
            img.src = l.cover_img_path;

            const textArea = document.createElement("div");
            textArea.id="text_area";

            const title = document.createElement("strong");
            title.textContent = l.title;

            const price = document.createElement("strong");
            price.textContent = `${l.price} €`;

            const carDef = document.createElement("strong");
            carDef.textContent = `${l.brand} ${l.model}`;

            const mileage = document.createElement("strong");
            mileage.textContent = `${l.mileage} km`;

            listing.appendChild(img);
            textArea.appendChild(title);
            textArea.appendChild(document.createElement("br"));
            textArea.appendChild(document.createElement("br"));
            textArea.appendChild(price);
            textArea.appendChild(document.createElement("br"));
            textArea.appendChild(document.createElement("br"));
            textArea.appendChild(carDef);
            textArea.appendChild(document.createElement("br"));
            textArea.appendChild(document.createElement("br"));
            textArea.appendChild(mileage);
            textArea.appendChild(document.createElement("br"));
            textArea.appendChild(document.createElement("br"));
            textArea.appendChild(document.createElement("hr"));
            textArea.appendChild(document.createElement("br"));

            const info1 = document.createElement("div");
            
            info1.innerHTML = ` <strong>${l.views}</strong> <svg xmlns="http://www.w3.org/2000/svg" style="width:1.5rem" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                                    </svg>`;
            info1.style="display: flex; align-items: center; gap: 5px";

            const info2 = document.createElement("div");

            info2.innerHTML = `<strong>${l.favorites}</strong> <svg xmlns="http://www.w3.org/2000/svg"  style="width:1.5rem" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                                                    </svg>`;
            info2.style="display: flex; align-items: center; gap: 5px";
            
            textArea.appendChild(info1);
            textArea.appendChild(info2);
            
            const editBtn = document.createElement("button");
            editBtn.innerHTML = "Edit";
            editBtn.classList.add("btn");
            editBtn.addEventListener("click", ()=>{
                window.location.href = `/editlistingp?listing_id=${l.listing_id}`;
            })
            textArea.appendChild(document.createElement("br"))
            textArea.appendChild(editBtn)

            listing.appendChild(textArea);

            document.getElementById("listings_area").appendChild(listing);
        }
        if(data.listings.length == 0)
        {
                const message = document.createElement("p");
                message.style = "color: white; text-align: center; font-size: large;"
                message.innerText = "You published no listings";
                document.getElementById("listings_area").appendChild(message);
        }
    });
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