
const passwordInput = document.getElementById("password_input");
const emailInput = document.getElementById("email_input");
const asterisk = document.getElementById("cpassword_astk");

let pin = false, ein = false;

passwordInput.addEventListener('input',()=>{

    if(passwordInput.value.length)
        pin = true;
    else
        pin = false;


    if(pin || ein)
        asterisk.style.display = "block";
    else
        asterisk.style.display = "none";
})

emailInput.addEventListener('input',()=>{

    if(ogEmail != emailInput.value)
        ein = true;
    else
        ein = false;

    if(pin || ein)
        asterisk.style.display = "block";
    else
        asterisk.style.display = "none";
})