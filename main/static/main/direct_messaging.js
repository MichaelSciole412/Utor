const data = document.currentScript.dataset;
const dmid = data.dmid;
console.log(dmid);
const websocket_url = `ws://${window.location.host}/ws/direct_message/${dmid}/`;

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
  if (message['type'] == "chat"){
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
