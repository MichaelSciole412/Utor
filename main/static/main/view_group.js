const data = document.currentScript.dataset;
const groupid = data.groupid;
const groupname = data.groupname;

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

function requestJoin(id){
  btn = document.getElementById("joinbutton");
  btn.classList.add("clickedbutton");
  btn.classList.remove("anchorbutton");
  btn.innerHTML = "Request Sent";
  btn.removeAttribute("onclick");

  req = new XMLHttpRequest();
  req.open("POST", `/ajax/request_join/${groupid}/`);
  req.send();
}

function reject(id){
  parentdiv = document.getElementById("requestlist");
  requestdiv = document.getElementById(`request${id}`);
  parentdiv.removeChild(requestdiv);

  num_requests = document.getElementById("num_requests");
  num_requests_int = parseInt(num_requests.innerHTML) - 1
  num_requests.innerHTML = num_requests_int
  if (num_requests_int == 0){
    none_div = document.createElement("template");
    none_div.innerHTML = `<div class="list2" id="request{{ usr.id }}">
                          <div style="width: 90%; padding: 7px; margin-left: 10px;">None</div>
                          </div>`;
    none_div = none_div.content.children[0];
    parentdiv.appendChild(none_div);
  }

  req = new XMLHttpRequest();
  req.open("POST", `/ajax/reject_request/${groupid}/${id}/`);
  req.send();
}

function accept(id, username){
  parentdiv = document.getElementById("requestlist");
  requestdiv = document.getElementById(`request${id}`);
  invitestuff = document.getElementById("invitestuff");
  parentdiv.removeChild(requestdiv);

  num_requests = document.getElementById("num_requests");
  num_requests_int = parseInt(num_requests.innerHTML) - 1
  num_requests.innerHTML = num_requests_int
  if (num_requests_int == 0){
    none_div = document.createElement("template");
    none_div.innerHTML = `<div class="list2">
                            <div style="width: 90%; padding: 7px; margin-left: 10px;">None</div>
                          </div>`;
    none_div = none_div.content.children[0];
    parentdiv.appendChild(none_div);
  }

  userlist_div = document.getElementById("userlist");
  new_user_div = document.createElement("template");
  new_user_div.innerHTML = `<div class="list2" id="listusr${id}">
                            <div style="width: 90%; padding: 7px; margin-left: 10px;"><a href='/profile/${id}' class="userlink">${username}</a></div>
                            <button onclick="kick(${id}, '${username}')" style="min-width: 80px;">Kick User</button>
                            </div>`
  new_user_div = new_user_div.content.children[0];
  userlist_div.insertBefore(new_user_div, invitestuff);

  req = new XMLHttpRequest();
  req.open("POST", `/ajax/accept_request/${groupid}/${id}/`);
  req.send();
}

function leave(){
  if (confirm("Are you sure you want to leave this Study Group?")){
    req = new XMLHttpRequest();
    req.open("POST", `/ajax/leave_group/${groupid}/`);
    req.send();
    location.reload();
  }
}

function kick(id, username){
  if (confirm(`Are you sure you want to kick ${username} from ${groupname}?`)) {
    userlist = document.getElementById("userlist");
    userdiv = document.getElementById(`listusr${id}`);
    userlist.removeChild(userdiv);

    req = new XMLHttpRequest();
    req.open("POST", `/ajax/kick_user/`);
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send(JSON.stringify({"group_id": groupid, "user_id": id}));
  }
}

function invite(){
  invite_input = document.getElementById("inviteuser");
  invite_text = document.getElementById("invite_text");
  if (invite_input.value != ""){
    req = new XMLHttpRequest();

    req.open("POST", `/ajax/invite/`);
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.onload = function() {
          invite_input.value = ""
          invite_text.innerHTML = this.responseText;
          setInterval(function() {
              invite_text.innerHTML = "";
          }, 3000);
      };
    req.send(JSON.stringify({"group_id": groupid, "username": invite_input.value}));
  }

}
