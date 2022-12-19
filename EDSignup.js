
// 가입부분 체크

function signUpCheck(){

  let nickname=document.getElementById("nickname").value  
  let name = document.getElementById("idname").value
  let password = document.getElementById("password").value
 
  let check = true;
    
//닉네임 확인
  if(nickname===""){
    document.getElementById("nicknameError").innerHTML="닉네임이 올바르지 않습니다."
    check = false
  }else{
    document.getElementById("nicknameError").innerHTML=""
  }

 
  // id확인
  if(idname===""){
    document.getElementById("idnameError").innerHTML="아이디가 올바르지 않습니다."
    check = false
  }else{
    document.getElementById("idnameError").innerHTML=""
  }


//비밀번호 체크
  if(password===""){
    document.getElementById("passwordError").innerHTML="비밀번호를 입력해주세요."
    check = false
  }else{
    document.getElementById("passwordError").innerHTML=""
  }
  

  if(check){
   
    document.getElementById("idnameError").innerHTML=""
    document.getElementById("passwordError").innerHTML=""
    document.getElementById("nicknameError").innerHTML=""
      
    //비동기 처리이벤트
    setTimeout(function() {
      alert("가입이 완료되었습니다.")
  },0);
  }
}