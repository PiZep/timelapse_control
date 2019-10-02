// $(window).load (function () { $('body').addClass ('all-loaded'); });

function convertToImgPerTime (interval) {
  var changedFreq = freq;
  var freqText = '';
  if (interval > 60) {
    freqText = 'img/hr';
    changedFreq = (3600 / interval);
  } else {
    freqText = 'img/min';
    changedFreq = (60 / interval);
  }
  var formatFreq = changedFreq.toFixed(2);
  document.querySelector('#freq').innerHTML = formatFreq.concat(' ', freqText);
}

function showOrHide (block) {
  var checkBox = document.getElementById('days');
  if (checkBox.checked === true) {
    visibility = 'block';
  } else {
    visibility = 'none';
  }
  document.getElementById(block).style.display = visibility;
}

window.onload = function (event) {
  convertToImgPerTime (document.getElementById('interval').value);
  showOrHide ('block');
}
