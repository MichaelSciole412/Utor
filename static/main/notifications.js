function removeNotification(id){
  list = document.getElementById("notificationlist");
  notif = document.getElementById(`notification${id}`);
  list.removeChild(notif);

  num_notifs = document.getElementById("num_notifications");

  req = new XMLHttpRequest();
  req.open("POST", `/ajax/delete_notification/${id}/`);
  req.send();

  new_num = parseInt(num_notifications.innerHTML) - 1
  num_notifications.innerHTML = new_num;

  if (new_num == 0){
    list.innerHTML = `<div class="cardlist2">
                        <p>No new notifications</p>
                      </div>`
    document.getElementById("notification_dot").innerHTML = "";
  }


}
