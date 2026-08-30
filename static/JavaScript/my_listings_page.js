fetch(`/API/get_listings?page=1&seller_id=${userId}&lpp=5`)
.then( response => response.json())
.then( data => {

    for (const l of data)
    {
        const listing = document.createElement("div");
        listing.classList.add("listing");

        const img = document.createElement("img");
        img.classList.add("image");
        img.src = l.cover_img_path;

        const text_area = document.createElement("div");
        text_area.id="text_area";

        const title = document.createElement("strong");
        title.textContent = l.title;

        const price = document.createElement("strong");
        price.textContent = `${l.price} €`;

        const car_def = document.createElement("strong");
        car_def.textContent = `${l.brand} ${l.model}`;

        const mileage = document.createElement("strong");
        mileage.textContent = `${l.mileage} km`;

        listing.appendChild(img);
        text_area.appendChild(title);
        text_area.appendChild(document.createElement("br"));
        text_area.appendChild(document.createElement("br"));
        text_area.appendChild(price);
        text_area.appendChild(document.createElement("br"));
        text_area.appendChild(document.createElement("br"));
        text_area.appendChild(car_def);
        text_area.appendChild(document.createElement("br"));
        text_area.appendChild(document.createElement("br"));
        text_area.appendChild(mileage);
        text_area.appendChild(document.createElement("br"));
        text_area.appendChild(document.createElement("br"));
        text_area.appendChild(document.createElement("hr"));
        text_area.appendChild(document.createElement("br"));

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
        
        text_area.appendChild(info1);
        text_area.appendChild(info2);
        
        const edit_btn = document.createElement("button");
        edit_btn.innerHTML = "Edit";
        edit_btn.classList.add("btn");
        edit_btn.addEventListener("click", ()=>{
            window.location.href = `/editlistingp?listing_id=${l.listing_id}`;
        })
        text_area.appendChild(document.createElement("br"))
        text_area.appendChild(edit_btn)

        listing.appendChild(text_area);

        listings_area.appendChild(listing);
    }
});