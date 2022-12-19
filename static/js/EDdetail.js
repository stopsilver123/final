function click_hearton(name){
    document.getElementById('heartIconOff').src='https://cdn-icons-png.flaticon.com/512/833/833472.png';
    window.location.replace("/EDdetail/<name>/");

}

function click_heartoff(name){
    document.getElementById('heartIconOff').src='https://cdn-icons-png.flaticon.com/512/535/535285.png';

}

const heartButtonOn = document.getElementById("heartButtonOn");
heartButtonOn.addEventListner("click", click_hearton);

const heartButtonOff = document.getElementById("heartButtonOff");
heartButtonOff.addEventListner("click", click_heartoff);
