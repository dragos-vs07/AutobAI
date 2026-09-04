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

const updateOtherModelVisibility = () => {
    if(modelsddl.value == "Other")
        document.getElementById("other_model").style = "display: block";
    else
        document.getElementById("other_model").style = "display: none";
}

modelsddl.addEventListener('change', updateOtherModelVisibility);

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

    updateOtherModelVisibility();
}

const updateOtherBrandVisibility = () => {
    if (makesddl.options[makesddl.selectedIndex].dataset.brand == "Other")
    {
        document.getElementById("other_brand").style="display: block";
        document.getElementById("other_model").style="display: block";
    }
    else
        document.getElementById("other_brand").style="display: none";
}

makesddl.addEventListener('change', function(){

    document.getElementById("other_model").style = "display: none";

    display_models(makesddl.options[makesddl.selectedIndex].dataset.brand);

    updateOtherBrandVisibility();
});

display_models(makesddl.options[makesddl.selectedIndex].dataset.brand);
updateOtherBrandVisibility();

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

const updateFuelOtherVisibility = () => {
    if(ft.value == "Other")
        document.getElementById("other_fuel").style = "display: block";
    else
        document.getElementById("other_fuel").style = "display: none";
}

ft.addEventListener('change', updateFuelOtherVisibility);
updateFuelOtherVisibility();

const engc = document.getElementById("engine_config");

const updateEngineConfigOtherVisibility = () => {
    if(engc.value == "Other")
        document.getElementById("other_config").style = "display: block";
    else
        document.getElementById("other_config").style = "display: none";
}

engc.addEventListener('change', updateEngineConfigOtherVisibility);
updateEngineConfigOtherVisibility();

const dt = document.getElementById("drivetrain");

const updateDrivetrainOtherVisibility = () => {
    if(dt.value == "Other")
        document.getElementById("other_drivetrain").style = "display: block";
    else
        document.getElementById("other_drivetrain").style = "display: none";
}

dt.addEventListener('change', updateDrivetrainOtherVisibility);
updateDrivetrainOtherVisibility();

const trans = document.getElementById("trans");

const updateTransOtherVisibility = () => {
    if(trans.value == "Other")
        document.getElementById("other_trans").style = "display: block";
    else
        document.getElementById("other_trans").style = "display: none";
}

trans.addEventListener('change', updateTransOtherVisibility);
updateTransOtherVisibility();

const bs = document.getElementById("bs");

const updateBodyStyleOtherVisibility = () => {
    if(bs.value == "Other")
        document.getElementById("other_bs").style = "display: block";
    else
        document.getElementById("other_bs").style = "display: none";
}

bs.addEventListener('change', updateBodyStyleOtherVisibility);
updateBodyStyleOtherVisibility();

title_input = document.getElementById("title_box");

const updateTitleCounter = () => {
    document.getElementById("char_counter_t").textContent = `${title_input.value.length}/80`
}

title_input.addEventListener("input", updateTitleCounter);
updateTitleCounter();

description_input = document.getElementById("descp_box");

const updateDescCounter = () => {
    document.getElementById("char_counter_d").textContent = `${description_input.value.length}/1000`
}

description_input.addEventListener("input", updateDescCounter);
updateDescCounter();



cidc = document.getElementById("cover_image_del_checkbox"); 
cidc.addEventListener('change', () => {
    if(cidc.checked)
        document.getElementById("new_cvr").style="display:block";
    else
        document.getElementById("new_cvr").style="display:none";
})

const Checkboxes = document.querySelectorAll('.delete_checkbox');
const SecImgInput = document.getElementById("sec_img_input");
const CvrImgInput = document.getElementById("cvr_img_input");
const fc = document.getElementById("file_count");

function CountLoadedImages()
{
    cnt = 0;
    document.querySelectorAll('.delete_checkbox').forEach(checkbox => { 
        if(!checkbox.checked)
            cnt = cnt + 1;
    })
    cnt += SecImgInput.files.length;
    cnt += CvrImgInput.files.length;

    return cnt;
}

fc.innerText = `${CountLoadedImages()} / 11 Images`;

SecImgInput.addEventListener('change', () => {

        const cnt = CountLoadedImages();

        fc.innerText = `${cnt}/11 Images`;

         if(cnt==11)
            document.getElementById("new_sec_img").style="display:none";
         else if(cnt<11)
            document.getElementById("new_sec_img").style="display:block"; 
        else
        {
            alert("You can upload at most 11 images ( 1 cover + 10 secondary )");
            SecImgInput.value = '';
            fc.innerText = `${CountLoadedImages()} / 11 Images`;
        }

        if(SecImgInput.files.length > 0)
            document.getElementById("cancel_sec").style = "display:flex;";
        else
            document.getElementById("cancel_sec").style = "display:none;";
    });

CvrImgInput.addEventListener('change', () => {
    if(CvrImgInput.files.length > 0)
        document.getElementById("cancel_cvr").style="display:flex";

    fc.innerText = `${CountLoadedImages()} / 11 Images`;
})

Checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {

        checkbox.closest('.image-item').classList.toggle('marked-for-deletion', checkbox.checked);

        const cnt = CountLoadedImages();
        fc.innerText = `${cnt} / 11 Images`;

        if(cnt>=11)
            document.getElementById("new_sec_img").style="display:none";
        else
            document.getElementById("new_sec_img").style="display:block"; 
    });
});

function clear_sec_input()
{
    SecImgInput.value = '';
    fc.innerText = `${CountLoadedImages()} / 11 Images`;

    if(CountLoadedImages() < 11)
        document.getElementById("new_sec_img").style = "display:block"; 

     document.getElementById("cancel_sec").style = "display:none;";
}
function clear_cvr_input()
{
    CvrImgInput.value= '';
    fc.innerText = `${CountLoadedImages()}/11 Images`;

    document.getElementById("cancel_cvr").style = "display:none;";
}
function close_modal()
{
    document.getElementById("delete_modal_box").style="display:none;";
     document.getElementById("modal_shadow").style="background: rgba(0, 0, 0, 0.0);display: none;"
}

function show_confirm_delete_listing(listing_id)
{
   document.getElementById("delete_modal_box").style="display:flex;flex-direction:column;align-items: center;";
   document.getElementById("modal_shadow").style="background: rgba(0, 0, 0, 0.7);display: flex;align-items: center;justify-content: center;z-index: 1000;"
}

document.getElementById("modal_shadow").addEventListener("click",(e)=>{
    const box = document.getElementById("delete_modal_box");
    if(!box.contains(e.target))
        close_modal();
});

function delete_listing(listing_id)
{
    fetch(`/delete_listing/${listing_id}`, { method: "POST"}).then(response => response.json().then(data=>{
        if(data.status == "success")
            window.location.href = "/mylistingsp";
        else
            alert(`Deleting listing failed, ${response.message}`);
    }))
}
