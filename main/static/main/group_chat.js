const data = document.currentScript.dataset;
const groupid = data.groupid;
const groupname = data.groupname;

const websocket_url = `ws://${window.location.host}/ws/group_chat/${groupid}/`;

const socket = new WebSocket(websocket_url);

const chatinput = document.getElementById("chatinput");
const chatusersdisplay = document.getElementById("chatusersdisplay");
const groupchatbox = document.getElementById("groupchatbox");

groupchatbox.scrollTop = groupchatbox.scrollHeight;

function sendMessage(){
  message = chatinput.value;
  if (/\S/g.test(message)){
    chatinput.value = "";
    socket.send(JSON.stringify({'message': message}));
  }
}

socket.onmessage = function(e){
  message = JSON.parse(e['data']);
  if (message['type'] == "join"){
    if (!document.getElementById(message["check_id"])){
      html = message['html'];
      user_joined = document.createElement("template");
      user_joined.innerHTML = html;
      user_joined = user_joined.content.children[0];

      chatusersdisplay.appendChild(user_joined);
    }
  } else if (message['type'] == "leave"){
    id_to_delete = message['id_to_delete'];
    listed_user = document.getElementById(id_to_delete);
    chatusersdisplay.removeChild(listed_user);
  } else if (message['type'] == "chat"){
    html = message['html'];
    new_chat = document.createElement("template");
    new_chat.innerHTML = html;
    new_chat = new_chat.content.children[0];
    groupchatbox.appendChild(new_chat);
    groupchatbox.scrollTop = groupchatbox.scrollHeight;
  }
}


chatinput.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) {
   sendMessage();
  }
});
