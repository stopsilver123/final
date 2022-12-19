function addOutput(num) {
  var display = document.getElementById("display");
  display.value = display.value + num;
}

function reset() {
  var display = document.getElementById("display");
  display.value = "";
  var displayResult = document.getElementById("result");
  displayResult.value = "";
}
