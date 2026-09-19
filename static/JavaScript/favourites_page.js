fetch(`/API/get_listings?seller_id=${userId}&page=1&lpp=5&favourites=True`)
.then( response => response.json())
.then(data => {
    const container = document.getElementById("listings_area");
    container.innerHTML = "";

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
})