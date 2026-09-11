
makesddl = document.getElementById("makes_dropdown_list");
modelsddl = document.getElementById("models_dropdown_list");

async function display_models(brand)
{
    modelsddl.innerHTML = "";

    if(brand != "Other" && brand != "Unknown")
    {
            const response = await fetch(`/API/get_models/${brand}`);
            const models = await response.json();

            for (const m of models)
            {
                const option = document.createElement("option");
                option.value = m.model;
                option.textContent = m.model;
                option.className = "input_box";
                modelsddl.appendChild(option);
            }
    }

    let option = document.createElement("option");
    option.value = "Other";
    option.textContent = "Other";
    option.className = "input_box";
    modelsddl.appendChild(option);

    option = document.createElement("option");
    option.value = "Unknown";
    option.textContent = "Unknown";
    option.className = "input_box";
    modelsddl.appendChild(option);
}

makesddl.addEventListener('change', function(){ 
    display_models(makesddl.options[makesddl.selectedIndex].dataset.brand);
});

display_models(makesddl.options[makesddl.selectedIndex].dataset.brand);

document.getElementById("form").addEventListener("submit",async function(e){
    e.preventDefault();

    const formData = new FormData(e.target);
    const params = new URLSearchParams(formData);

    const response = await fetch(`/API/predict_price?${params}`);
    const data = await response.json();

    console.log(data.predicted_price);
})