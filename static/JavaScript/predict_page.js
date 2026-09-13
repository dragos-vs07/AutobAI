
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

    document.getElementById("display_pred_box").textContent = `Your car evaluated at a price of ${data.predicted_price}€`
    document.getElementById("modal").style="display:flex;flex-direction:column;align-items: center;";
    document.getElementById("modal_shadow").style="background: rgba(0, 0, 0, 0.7);display: flex;align-items: center;justify-content: center;z-index: 1000;"

    requestAnimationFrame(() => {
        document.getElementById("modal").classList.add("show");
    });
})

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) 
      entry.target.classList.add('visible');
    else
        entry.target.classList.remove('visible');
  });
}, {
  threshold: 0.05, // trigger when 15% of the element is visible
  rootMargin: '0px 0px -50px 0px' // trigger slightly before it fully enters
});

document.querySelectorAll('.fade_in').forEach(el => observer.observe(el));

function close_modal()
{
    document.getElementById("modal").style="display:none;";
    document.getElementById("modal").classList.remove("show");
    document.getElementById("modal_shadow").style="background: rgba(0, 0, 0, 0.0);display: none;"
}
document.getElementById("modal_shadow").addEventListener("click",(e)=>{
    const box = document.getElementById("modal");
    if(!box.contains(e.target))
        close_modal();
});
