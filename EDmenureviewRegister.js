//이미지 미리보기
$(function() {
    $("#photo").on('change', function(){
    readURL(this);
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
        $('#menupreview').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

//메뉴등록버튼
function registrationYN(){
    var result = confirm("등록하시겠습니까?");

    if (result == true){
        var checked = checkformRegistered();

        if(checked == true) {alert("메뉴를 등록합니다.");}
        else if(checked == false) {alert("필수 항목을 모두 채워주세요.");}
    }
    else {
        alert("취소되었습니다.");
    }
}

function checkformRegistered(){
    var valueTF = true;

    if(frm.foodname.value==""){
        valueTF = false;
    }
    if(frm.price.value==""){
        valueTF = false;
    }
    if((frm.category[0].checked == false) && (frm.category[1].checked == false)) {
          valueTF = false;
    }
     if((frm.vegan[0].checked == false) && (frm.vegan[1].checked == false)) {
        valueTF = false;
    } 

    return valueTF;
}

//리뷰등록버튼
function registrationYNreview(){
    var result = confirm("등록하시겠습니까?");

    if (result == true){
        var checked = checkformRegisteredreview();

        if(checked == true) {alert("등록되었습니다.");}
        else if(checked == false) {alert("필수 항목을 모두 채워주세요.");}
    }
    else {
        alert("취소되었습니다.");
    }
}

function checkformRegisteredreview(){
    var valueTF = true;

    if(frm.foodname.value==""){
        valueTF = false;
    }

     if((frm.rating[0].checked == false) && (frm.rating[1].checked == false) && (frm.rating[2].checked == false)&& (frm.rating[3].checked == false) && (frm.rating[4].checked == false)) {
        valueTF = false;
    } 

    return valueTF;
}














