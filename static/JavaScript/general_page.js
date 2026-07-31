
fetch("API/get_public_listings?page=1")
.then( response => response.json())
.then(data => {
    const container = document.getElementById("listings_area");
    container.innerHTML = "";

    for (const listing of data)
        {
            const cover_img = document.createElement("img");
            cover_img.src = listing.cover_img_path;

            console.log("path here:" , listing.cover_img_path)
            container.appendChild(cover_img);

        } 
})