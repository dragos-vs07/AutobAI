
pb = document.getElementById("PriceRange");
pn = document.getElementById("PriceNumber");

pb.addEventListener('input' , () => {
    pn.value = pb.value;
})

pn.addEventListener('input' , () => {
    pb.value = pn.value;
})

ed = document.getElementById("ed");

unitL = document.getElementById("unitL");
unitCC = document.getElementById("unitCC");

unitL.addEventListener('change' , () => {
    ed.placeholder = "L";
})

unitCC.addEventListener('change' , () => {
    ed.placeholder = "cc";
})

fe = document.getElementById("fe");

unitLkm = document.getElementById("unitLkm");
unitmpg = document.getElementById("unitmpg");

unitLkm.addEventListener('change' , () => {
    fe.placeholder = "l/100km";
})

unitmpg.addEventListener('change' , () => {
    fe.placeholder = "mpg";
})

ep = document.getElementById("ep");

unithp = document.getElementById("unithp");
unitkW = document.getElementById("unitkW");

unithp.addEventListener('change' , () => {
    ep.placeholder = "hp(PS)";
})

unitkW.addEventListener('change' , () => {
    ep.placeholder = "kW";
})

makesddl = document.getElementById("makes_dropdown_list");
modelsddl = document.getElementById("models_dropdown_list");

modelsddl.addEventListener('change' , () => {

    if(modelsddl.value == "Other")
        document.getElementById("other_model").style = "display: block";
    else
        document.getElementById("other_model").style = "display: none";
})
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
                option.value = m.id;
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

    document.getElementById("other_model").style = "display: none";

    display_models(makesddl.options[makesddl.selectedIndex].dataset.brand);

    if (makesddl.options[makesddl.selectedIndex].dataset.brand == "Other")
    {
        document.getElementById("other_brand").style="display: block";
        document.getElementById("other_model").style="display: block";
    }
    else
        document.getElementById("other_brand").style="display: none";
});

display_models(makesddl.options[makesddl.selectedIndex].dataset.brand);

mlg = document.getElementById("mileageInput");

unitkm = document.getElementById("unitkm");
unitmiles = document.getElementById("unitmiles");

unitkm.addEventListener('change' , () => {
    mlg.placeholder = "km";
})

unitmiles.addEventListener('change' , () => {
    mlg.placeholder = "miles";
})

const ft = document.getElementById("fuel_type");

ft.addEventListener('change' , () => {
    if(ft.value == "Other")
        document.getElementById("other_fuel").style = "display: block";
    else
        document.getElementById("other_fuel").style = "display: none";
})

const engc = document.getElementById("engine_config");

engc.addEventListener('change' , () => {
    if(engc.value == "Other")
        document.getElementById("other_engine_config").style = "display: block";
    else
        document.getElementById("other_engine_config").style = "display: none";
})

const dt = document.getElementById("drivetrain");

dt.addEventListener('change' , () => {
    if(dt.value == "Other")
        document.getElementById("other_drivetrain").style = "display: block";
    else
        document.getElementById("other_drivetrain").style = "display: none";
})

const trans = document.getElementById("trans");

trans.addEventListener('change' , () => {
    if(trans.value == "Other")
        document.getElementById("other_trans").style = "display: block";
    else
        document.getElementById("other_trans").style = "display: none";
})

const bs = document.getElementById("bs");

bs.addEventListener('change' , () => {
    if(bs.value == "Other")
        document.getElementById("other_bs").style = "display: block";
    else
        document.getElementById("other_bs").style = "display: none";
})