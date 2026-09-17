
function getAndDisplayListings(pageNumber=1,listingsPerPage=24,userInput='')
{
    fetch(`/API/get_listings?page=${pageNumber}&lpp=${listingsPerPage}&ui=${userInput}`)
    .then( response => response.json())
    .then(data => {
        const container = document.getElementById("listings_area");
        container.innerHTML = "";

        for (const listing of data)
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
        if(data.length == 0)
        {
            const message = document.createElement("p");
            message.style = "color: white; text-align: center; font-size: large;"
            message.innerText = "No listings were found";
            container.appendChild(message);
        } 
    })
}

function checkFavourite(event)
{
    event.stopPropagation();
    const svg = event.currentTarget;
    const listingId = svg.dataset.listingId;

    fetch(`/API/toggle_favourite?listing_id=${listingId}`)
    .then(response => {
        if(response.ok)
        {
            response.json().then(data=>{
            if(data.favourited == true)
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

let timeoutId;

const searchBar = document.getElementById("search_bar");
searchBar.addEventListener('input', ()=>{
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
        getAndDisplayListings(1,24,searchBar.value);   // searches after 1s after the user made the last change to input
    }, 1000);

})

getAndDisplayListings(1,24);

// retrieving and displaying models based on a chosen brand

const modelsCheckboxList = document.getElementById("models_checkbox_list");
const makesCheckboxList = document.getElementById("makes_checkbox_list");

makesCheckboxList.addEventListener('change', (e)=>{
    if(!e.target.matches('input[type="checkbox"]')) return;
    
    const anyCheckbox = document.getElementById("any_make_checkbox");
    let checkedMakes = [];

    if(e.target == anyCheckbox) //if the user toggled the checkbox
    {
        if(anyCheckbox.checked)  // user just toggled on the any checkbox => all toggled on
            for(c of document.querySelectorAll(".make_checkbox"))
                c.checked = true;
        else if(!anyCheckbox.checked) // user just toggled off the any checkbox => all toggled off
            for(c of document.querySelectorAll(".make_checkbox"))
                c.checked = false;
    }
    else    //otherwise the user toggled some other singular option
        if(anyCheckbox.checked) //if the any checkbox was checked, it cant be now because the user muts've unchecked something
            anyCheckbox.checked = false;

    checkedMakes = Array.from(
    document.querySelectorAll('#makes_checkbox_list input:checked:not(#any_make_checkbox)')
    ).map(cb => cb.dataset.brand);

    modelsCheckboxList.innerHTML="";

    console.log(checkedMakes);

    for (brand of checkedMakes)
    addModels(brand);
})

function addModels(brand)
{
    fetch(`/API/get_models/${brand}`).then( response => {
        if(response.ok)
        {
            let label = document.createElement("label");
            label.style="display: block";
            const modelOption = document.createElement("input");
            modelOption.type = "checkbox";
            modelOption.classList.add("input_box");
            modelOption.name = "model";
            modelOption.value = "Any";
            modelOption.checked = true;
            modelOption.dataset.model = "Any";
            label.appendChild(modelOption);
            label.appendChild(document.createTextNode("Any"));
            modelsCheckboxList.appendChild(label);

            response.json().then(data =>{
                    for (model of data)
                    {
                        label = document.createElement("label");
                        label.style="display: block";
                        const modelOption = document.createElement("input");
                        modelOption.type = "checkbox";
                        modelOption.classList.add("input_box");
                        modelOption.name = "model";
                        modelOption.checked = true;
                        modelOption.value = model.id;
                        modelOption.dataset.model = model.model;
                        label.appendChild(modelOption);
                        label.appendChild(document.createTextNode(model.model));
                        modelsCheckboxList.appendChild(label);
                    } 
            })
        }
        else
        response.json().then(data => {
            alert(`Model retrieval failed, ${data.message}`);
            })
        
    })
        
}

// end of model displaying

// dynamic searching in the filter options

for(const ipt of document.querySelectorAll(".filter_input"))
{
    ipt.addEventListener('input',()=>{
        if(ipt.value.length)
            for(const c of document.getElementById(ipt.dataset.cblist).children)
            {
                let value = "";

                if(c.querySelector('input').dataset.brand)
                    value = c.querySelector('input').dataset.brand;
                else
                    value = c.querySelector('input').value;

                    if( ! value.toLowerCase().includes(ipt.value.toLowerCase()) )
                        c.style.display = "none";
                    else
                        c.style.display = "block";

            }
        else
            for(const c of document.getElementById(ipt.dataset.cblist).children)
                c.style.display = "block";
    })
}

// displaying / hiding the dropdown lists on filter options

document.addEventListener("click",(e)=>{

    for( ipt of document.querySelectorAll(".filter_input"))
    {
        const checkboxList = document.getElementById(ipt.dataset.cblist);
        if(ipt.contains(e.target))
            checkboxList.classList.add("show_checkbox_list");
        else if(!checkboxList.contains(e.target))
            checkboxList.classList.remove("show_checkbox_list");
    }
})

for(const ddl of document.querySelectorAll(".dropdown_checkbox_list"))
{
    if(ddl.id != "makes_checkbox_list")
    ddl.addEventListener("click",(e)=>{
        for(const label of ddl.children)
            {
                
                const c = label.querySelector('input');
                if(c.value == "Any" && e.target === c)   //if the any checkbox was clicked
                    {
                        

                        if(c.checked)   // if it was toggled on
                            for(const label2 of ddl.children)
                            {
                                const c2 = label2.querySelector('input');
                                c2.checked = true;  //all checked
                            }
                        else    //else if it was toggled off
                            for(const label2 of ddl.children)
                            {
                                const c2 = label2.querySelector('input');
                                c2.checked = false; // all unchecked
                            }
                    }  
            }
    })
}

for( const minInput of document.querySelectorAll(".min_input"))
{
    const maxInput = document.getElementById(minInput.dataset.max);

    minInput.addEventListener("change",()=>{
        if(minInput.value > maxInput.value)
            maxInput.value = minInput.value;
    })

    maxInput.addEventListener("change",()=>{
        if(minInput.value > maxInput.value)
            maxInput.value = minInput.value;
    })
}

// DE COMPLETAT

function apply_filters()
{
    const categoricalFilterOptions = ["make","model","body_style","fuel_type","engine_config","transmission","drivetrain"]
    const numericalFilterOptions = ["power","year","price","displacement","fuel_ef"]

    /*for(const c of categoricalFilterOptions)
    {
        const chosenValues = Array.from(
        document.querySelectorAll(`input[name="${c}"]:checked`)
        ).map(cb => cb.value);
    }
        ASA IAU OPTIUNILE ALESE
    */  
}
