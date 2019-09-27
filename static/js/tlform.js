
window.onload = function(event) {
  convertToImgPerMin(document.getElementById('interval').value);
  showOrHide('block');
}

function convertToImgPerMin(interval) {
  document.querySelector("#freq").innerHTML = 60/interval;
}

function showOrHide(block) {
  var checkBox = document.getElementById("days");
  if (checkBox.checked == true) {
    visibility = "block";
  } else {
    visibility = "none";
  }
  document.getElementById(block).style.display = visibility;
}
