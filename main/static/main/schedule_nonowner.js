const data = document.currentScript.dataset;
const groupid = data.groupid;

const select_past = document.getElementById("select_past");

select_past.onchange = function(){
  link = select_past.value;
  window.location = link;
}
