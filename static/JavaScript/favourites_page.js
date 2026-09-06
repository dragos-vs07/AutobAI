fetch(`/API/get_listings?seller_id=${userId}&page=1&lpp=5&favourites=True`)
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
            cover_img.classList.add("image");

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
            cell.appendChild(document.createElement("br"));
            cell.addEventListener('click',()=>{
                window.location.href = `/viewlisting?listing_id=${listing.listing_id}`;
            })
            container.appendChild(cell);
        } 
})