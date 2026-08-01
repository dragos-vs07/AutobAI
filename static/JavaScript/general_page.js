
fetch("API/get_public_listings?page=1")
.then( response => response.json())
.then(data => {
    const container = document.getElementById("listings_area");
    container.innerHTML = "";

    for (const listing of data)
        {
            const cell = document.createElement("div");

            cell.style = "color: white; border: 1px solid #c9a227; padding: 10px; border-radius: 10px; display: flex; flex-direction: column; align-items: center; cursor: pointer ";

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

            container.appendChild(cell);
        } 
})