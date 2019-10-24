function toggleActive(itemId, pg){
  var buttons = document.getElementsByClassName('mode-select');
  for (var i = 0; i < buttons.length; i++){
    buttons[i].classList.remove('active')
  }
  var item = document.getElementById(itemId);
  item.classList.toggle("active");
  var pages = []
  modes = document.getElementsByClassName("mode-select")
  for (var i=0; i < modes.length; i++){
  	pages.push(modes[i].id.toLowerCase() + "pg")
  }
  for (var i=0; i < pages.length; i++){
    document.getElementsByClassName(pages[i])[0].style.display="none";
  }
  document.querySelectorAll(pg)[0].style.display="unset";
}


var sources = document.getElementsByClassName("colorbox");
for (var i = 0; i < sources.length; i++){
  var source = sources[i]
    picker = new CP(source);
// prevent showing native color picker panel
source.onclick = function(e) {
    e.preventDefault();
};
picker.on("change", function(color) {
  this.source.style.backgroundColor = '#' + color;
});
}

function rgbStrToHex(color){
  color = color.replace("rgb(","");
  color = color.replace(")","");
  color = color.split(",");
  color = CP.RGB2HEX(color);
  return color;
}

function sendSolid(){
  var color = document.getElementsByClassName("solidbtn")[0].style.backgroundColor;
  eel.solid(rgbStrToHex(color));
}

function listAppend(listId, btnClass){
  value = document.getElementById(listId).value;
  if (value.length > 0){
    value += ', '
  }
  document.getElementById(listId).value = value + rgbStrToHex(document.getElementsByClassName(btnClass)[0].style.backgroundColor);
}

function sendPulses(listId){
  listStr = document.getElementById(listId).value;
  listStr = listStr.replace(/[\t]/g, '');
  list = listStr.split(/[\ \n\,]+/g);
  eel.pulse(list);
}
