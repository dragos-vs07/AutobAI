const CATEGORICAL_FILTERS = ["make", "model", "body_style", "fuel_type", "engine_config", "transmission", "drivetrain"];
const NUMERICAL_FILTERS = ["power", "year", "price", "mileage", "displacement", "fuel_ef"];

let savedFilterOptions = {};
let timeoutId;
let currentTotal;
let currentPage = 1;

const searchBar = document.getElementById("search_bar");
const sortSelect = document.getElementById("sort_listings_select");
const modelsCheckboxList = document.getElementById("models_checkbox_list");
const makesCheckboxList = document.getElementById("makes_checkbox_list");
const LPP = 24;

function createListingElements(data)
{
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
        carDef.style = "display:flex; flex-direction:row; gap: 5px;";

        const brand = document.createElement("p");
        brand.textContent = listing.brand;
        carDef.appendChild(brand);

        const model = document.createElement("p");
        model.textContent = listing.model;
        carDef.appendChild(model);

        const mileage = document.createElement("p");
        mileage.textContent = `${listing.mileage} km`;

        cell.appendChild(title);
        cell.appendChild(coverImg);
        cell.appendChild(price);
        cell.appendChild(carDef);
        cell.appendChild(mileage);

        if (userId != null && userId != listing.seller_id)
        {
            const fav_icon = document.createElement("div");
            fav_icon.innerHTML = `<svg onclick="checkFavourite(event)" data-listing-id="${listing.listing_id}" xmlns="http://www.w3.org/2000/svg" class="pic" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12Z" />
                    </svg>`;
            fav_icon.classList.add("fav_icon");

            fav_icon.querySelector("svg").classList.add(
                listing.is_favourite == "True" ? "is-favourited" : "is-not-favourited"
            );

            cell.appendChild(fav_icon);
        }

        cell.appendChild(document.createElement("br"));
        cell.addEventListener('click', () => {
            window.location.href = `/viewlisting?listing_id=${listing.listing_id}`;
        });
        container.appendChild(cell);
    }

    if (data.length == 0)
    {
        const message = document.createElement("p");
        message.style = "color: white; text-align: center; font-size: large;";
        message.innerText = "No listings were found";
        container.appendChild(message);
    }
}

function getAndDisplayListings(pageNumber = 1, listingsPerPage = LPP, userInput = '', filterInput = {})
{
    const params = new URLSearchParams({
        page: pageNumber,
        lpp: listingsPerPage,
        ui: userInput,
        sort: sortSelect.value
    });

    for (const [key, values] of Object.entries(filterInput))
    {
        if (NUMERICAL_FILTERS.includes(key))
        {
            const [min, max] = values;
            if (min !== null) params.append(`min_${key}`, min);
            if (max !== null) params.append(`max_${key}`, max);
        }
        else
        {
            for (const v of values)
                params.append(key, v);
        }
    }

    fetch(`/API/get_listings?${params}`)
        .then(response => response.json())
        .then(data =>{ 
            createListingElements(data.listings);
            currentTotal = data.total;
            currentPage = pageNumber;

            document.getElementById("current_page").textContent = pageNumber;

            if(currentPage * LPP >= currentTotal) // it means there can be a next page
                document.getElementById("next_page_btn").classList.add("hide_button");
            else
                 document.getElementById("next_page_btn").classList.remove("hide_button");

            if(currentPage == 1)
                document.getElementById("previous_page_btn").classList.add("hide_button");
            else
                 document.getElementById("previous_page_btn").classList.remove("hide_button");
        });
}

function apply_filters()
{
    const filterOptions = {};

    for (const c of CATEGORICAL_FILTERS)
    {
        const chosen = Array.from(document.querySelectorAll(`input[name="${c}"]:checked`))
            .map(cb => cb.value)
            .filter(v => v !== "Any");

        if (chosen.length > 0)
            filterOptions[c] = chosen;
    }

    for (const c of NUMERICAL_FILTERS)
    {
        const minSel = document.querySelector(`[name="min_${c}"]`);   // doesn't exist for fuel_ef
        const maxSel = document.querySelector(`[name="max_${c}"]`);

        const min = minSel ? Number(minSel.value) : null;
        const max = maxSel ? Number(maxSel.value) : null;

        filterOptions[c] = [min, max];
    }

    savedFilterOptions = filterOptions;
    currentPage = 1;
    getAndDisplayListings(currentPage, LPP, searchBar.value, filterOptions);  // reset to page 1 when filters applied
}

function clear_filters()
{
    for (const cb of document.querySelectorAll('#filter_area input[type="checkbox"]'))
        cb.checked = true;

    // clear the text typed in the dropdown search boxes and un-hide options
    for (const ipt of document.querySelectorAll(".filter_input"))
        ipt.value = "";
    for (const label of document.querySelectorAll(".dropdown_checkbox_list > label"))
        label.style.display = "block";

    for (const nf of NUMERICAL_FILTERS)
    {
        const minSel = document.querySelector(`[name="min_${nf}"]`);
        const maxSel = document.querySelector(`[name="max_${nf}"]`);

        if (minSel) minSel.selectedIndex = 0;
        if (maxSel) maxSel.selectedIndex = maxSel.options.length - 1;
    }

    // rebuild the model list, and only apply once every model checkbox exists
    refreshModels().then(apply_filters);
}

function checkFavourite(event)
{
    event.stopPropagation();
    const svg = event.currentTarget;
    const listingId = svg.dataset.listingId;

    fetch(`/API/toggle_favourite?listing_id=${listingId}`)
    .then(response => {
        if (response.ok)
        {
            response.json().then(data => {
                if (data.favourited == true)
                    svg.classList.replace("is-not-favourited", "is-favourited");
                else
                    svg.classList.replace("is-favourited", "is-not-favourited");
            });
        }
        else
        {
            response.json().then(data => {
                alert(`Toggle favourite failed, ${data.message}`);
            });
        }
    });
}

searchBar.addEventListener('input', () => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
        currentPage = 1;
        getAndDisplayListings(currentPage, LPP, searchBar.value, savedFilterOptions);
    }, 1000);
});

sortSelect.addEventListener('change', () => {
    currentPage = 1;
    getAndDisplayListings(currentPage, LPP, searchBar.value, savedFilterOptions);
});

// ---------- models list ----------

function makeModelCheckbox(value, text)
{
    const label = document.createElement("label");
    label.style = "display: block";
    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.classList.add("input_box");
    cb.name = "model";
    cb.value = value;
    cb.checked = true;
    label.appendChild(cb);
    label.appendChild(document.createTextNode(text));
    return label;
}

function refreshModels()
{
    const checkedMakes = Array.from(
        document.querySelectorAll('#makes_checkbox_list input:checked:not(#any_make_checkbox)')
    ).map(cb => cb.value);

    modelsCheckboxList.innerHTML = "";

    modelsCheckboxList.appendChild(makeModelCheckbox("Any", "Any"));
    modelsCheckboxList.appendChild(makeModelCheckbox("Other", "Other"));

    return Promise.all(checkedMakes.map(brand => addModels(brand)));
}

function addModels(brand)
{
    if (brand == "Other")
        return Promise.resolve();

    return fetch(`/API/get_models/${encodeURIComponent(brand)}`).then(response => {
        if (response.ok)
        {
            return response.json().then(data => {
                for (const m of data)
                    modelsCheckboxList.appendChild(makeModelCheckbox(m.model, m.model));
            });
        }

        return response.json().then(data => {
            alert(`Models retrieval failed, ${data.message}`);
        });
    });
}

makesCheckboxList.addEventListener('change', (e) => {
    if (!e.target.matches('input[type="checkbox"]')) return;

    const anyCheckbox = document.getElementById("any_make_checkbox");

    if (e.target == anyCheckbox)
    {
        for (const c of document.querySelectorAll(".make_checkbox"))
            c.checked = anyCheckbox.checked;
    }
    else if (anyCheckbox.checked)
        anyCheckbox.checked = false;

    refreshModels();
});

function nextpage()
{
    const totalPages = Math.max(1, Math.ceil(currentTotal / LPP));
    if (currentPage >= totalPages) return;
    getAndDisplayListings(currentPage + 1, LPP, searchBar.value, savedFilterOptions);
    window.scrollTo(0, 0);
}

function previouspage()
{
    getAndDisplayListings(Math.max(1,currentPage - 1), LPP, searchBar.value, savedFilterOptions);
    window.scrollTo(0, 0);
}

// ---------- dropdown behaviour ----------

for (const ipt of document.querySelectorAll(".filter_input"))
{
    ipt.addEventListener('input', () => {
        const needle = ipt.value.toLowerCase();
        for (const c of document.getElementById(ipt.dataset.cblist).children)
        {
            const value = c.querySelector('input').value.toLowerCase();
            c.style.display = value.includes(needle) ? "block" : "none";
        }
    });
}

document.addEventListener("click", (e) => {
    for (const ipt of document.querySelectorAll(".filter_input"))
    {
        const checkboxList = document.getElementById(ipt.dataset.cblist);
        if (ipt.contains(e.target))
            checkboxList.classList.add("show_checkbox_list");
        else if (!checkboxList.contains(e.target))
            checkboxList.classList.remove("show_checkbox_list");
    }
});

for (const ddl of document.querySelectorAll(".dropdown_checkbox_list"))
{
    if (ddl.id == "makes_checkbox_list") continue;

    ddl.addEventListener("click", (e) => {
        const c = e.target;
        if (!c.matches('input[type="checkbox"]') || c.value != "Any") return;

        for (const cb of ddl.querySelectorAll('input[type="checkbox"]'))
            cb.checked = c.checked;
    });
}

for (const minInput of document.querySelectorAll(".min_input"))
{
    const maxInput = document.getElementById(minInput.dataset.max);

    const sync = () => {
        if (Number(minInput.value) > Number(maxInput.value))
            maxInput.value = minInput.value;
    };

    minInput.addEventListener("change", sync);
    maxInput.addEventListener("change", sync);
}


// ---------- initial load ----------

refreshModels();
getAndDisplayListings(currentPage, LPP);