const data = document.currentScript.dataset;
const groupid = data.groupid;

function escapeHTML(text) {
    return text
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

function unescapeHTML(text){
  return text
       .replace(/&amp;/g, "&")
       .replace(/&lt;/g, "<")
       .replace(/&gt;/g, ">")
       .replace(/&quot;/g, "\"")
       .replace(/&#039;/g, "'");
}

function editDesc(){
  b1 = document.getElementById("b1");
  desc = document.getElementById("desc");
  desc_text = document.getElementById("desc_text");

  desc_textarea = document.createElement("textarea");
  desc_textarea.value = unescapeHTML(desc_text.innerHTML);
  desc_textarea.id = "desc_textarea";
  desc_textarea.setAttribute("maxlength", "500");
  desc_textarea.rows = 5;
  desc.removeChild(desc_text);
  desc.insertBefore(desc_textarea, b1);
  b1.innerHTML = "Save";
  b1.setAttribute("onclick", "saveDesc();");
}

function saveDesc(){
  b1 = document.getElementById("b1");
  desc = document.getElementById("desc");
  desc_textarea = document.getElementById("desc_textarea");

  desc_text = document.createElement("p");
  desc_text.id = "desc_text";
  desc_text.innerHTML = escapeHTML(desc_textarea.value);

  req = new XMLHttpRequest();
  req.open("POST", `/ajax/save_desc/${groupid}/`);
  req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  req.send(JSON.stringify({"desc": desc_textarea.value}));


  desc.removeChild(desc_textarea);
  desc.insertBefore(desc_text, b1);
  b1.innerHTML = "Edit Description";
  b1.setAttribute("onclick", "editDesc();");
}
