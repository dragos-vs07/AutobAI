
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