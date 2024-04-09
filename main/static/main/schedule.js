const data = document.currentScript.dataset;
const groupid = data.groupid;

Date.prototype.stdTimezoneOffset = function () {
var jan = new Date(this.getFullYear(), 0, 1);
var jul = new Date(this.getFullYear(), 6, 1);
return Math.max(jan.getTimezoneOffset(), jul.getTimezoneOffset());
}

Date.prototype.isDstObserved = function () {
return this.getTimezoneOffset() < this.stdTimezoneOffset();
}

const meet_title = document.getElementById("meet_title");
const meet_date = document.getElementById("meet_date");
const meet_time = document.getElementById("meet_time");
const meet_duration_hours = document.getElementById("meet_duration_hours");
const meet_duration_minutes = document.getElementById("meet_duration_minutes");
const meet_location = document.getElementById("meet_location");
const meet_description = document.getElementById("meet_description");
const submit_meet = document.getElementById("submit_meet");
const scheduleform = document.getElementById("scheduleform");
const schedule_list = document.getElementById("schedule-list");
const schedule_item_input_div = document.getElementById("schedule-item-input-div");
const select_past = document.getElementById("select_past");

scheduleform.addEventListener("submit", (e) => {
  e.preventDefault();
  var meet_title_value = meet_title.value.slice(0, 50);
  var meet_date_value = meet_date.value;
  var date_arr = meet_date_value.split("-");
  var formatted_date = `${parseInt(date_arr[1])}/${parseInt(date_arr[2])}/${date_arr[0].slice(2)}`;
  var meet_time_value = meet_time.value;
  var meet_time_arr = meet_time_value.split(":");
  var meet_time_hour = parseInt(meet_time_arr[0]);
  var meet_time_min = meet_time_arr[1];
  var am_pm = meet_time_hour >= 12 ? 'PM' : 'AM';
  var formatted_meet_time_hour = meet_time_hour == 12 ? 12 : (meet_time_hour == 0 ? 12 : meet_time_hour % 12);
  var formatted_time = `${formatted_meet_time_hour}:${meet_time_min} ${am_pm}`;
  var meet_duration_hours_value = meet_duration_hours.value;
  var meet_duration_minutes_value = meet_duration_minutes.value;
  var meet_location_value = meet_location.value.slice(0, 100);
  var meet_description_value = meet_description.value.slice(0, 400);

  var date = new Date(meet_date_value + "T" + meet_time_value);
  var utc = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
  var utc_sec = utc.valueOf() / 1000 - (utc.isDstObserved() ? 3600 : 0);

  req = new XMLHttpRequest();
  req.open("POST", `/ajax/schedule/`);
  req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  req.onload = function() {
        if (this.responseText == "DENY"){
          return;
        }
        meeting_id = this.responseText;

        new_meeting = document.createElement("template");
        new_meeting.innerHTML = `<div datetimeorder="${utc_sec}" id="meeting${meeting_id}" class="schedule-item schedule-item-hover">
                                  <div class="flexrow center">
                                    <div class="center realllycenter"><h3 style="margin-top: 25px; margin-bottom: 5px; margin-left: 32px;">${meet_title_value}</h3></div>
                                    <div style="text-align: right; margin-top: 10px; margin-right: 5px;">
                                      <button class="xbutton" onclick="removeMeeting(${meeting_id});"><img src="/static/main/X_button.png" width=20px/></button>
                                    </div>
                                  </div>
                                  <div class="center realllycenter"><h5 style="margin-top: 5px; margin-bottom: 5px;">${formatted_date}&nbsp;${formatted_time}</h5></div>
                                  <div style="margin-top: auto; margin-bottom: auto;">
                                    <table class="schedule-table">
                                      <tr>
                                        <th>Duration</th>
                                        <td>${meet_duration_hours_value == 0 ? "" : meet_duration_hours_value + " hour" + (meet_duration_hours_value == 1 ? "" : "s")}${meet_duration_minutes_value == 0 ? "" : " " + meet_duration_minutes_value + " minute" + (meet_duration_minutes_value == 1 ? "" : "s")}
                                         </td>
                                      </tr>
                                      <tr>
                                        <th>Location</th>
                                        <td>${meet_location_value}</td>
                                      </tr>
                                      <tr>
                                        <th>Description</th>
                                        <td>${meet_description_value}</td>
                                      </tr>
                                    </table>
                                  </div>
                                </div>`;
        new_meeting = new_meeting.content.children[0];

        div_list = document.querySelectorAll("#schedule-list > div");

        for(var i = 0; i < div_list.length; i++) {
            var elem = div_list[i];
            var elem_order = elem.getAttribute("datetimeorder");
            if (elem_order === null) {
              schedule_list.insertBefore(new_meeting, elem);
              break;
            }
            elem_order = parseInt(elem_order);
            if (elem_order > utc_sec){
              schedule_list.insertBefore(new_meeting, elem);
              break;
            }
        }
  };
  req.send(JSON.stringify({"group_id": groupid,
                           "title": meet_title_value,
                           "time": meet_time_value,
                           "date": meet_date_value,
                           "duration_hours": meet_duration_hours_value,
                           "duration_minutes": meet_duration_minutes_value,
                           "location": meet_location_value,
                           "description": meet_description_value}));
  meet_title.value = "";
  meet_date.value = "";
  meet_time.value = "";
  meet_duration_hours.value = "";
  meet_duration_minutes.value = "";
  meet_location.value = "";
  meet_description.value = "";
});

function removeMeeting(id){
  if (confirm("Are you sure you want to delete this meeting from the schedule?")){
    toremove = document.getElementById("meeting" + id.toString());
    schedule_list.removeChild(toremove);

    req = new XMLHttpRequest();
    req.open("POST", `/ajax/remove_meeting/${id}/`);
    req.send();
  }

}

select_past.onchange = function(){
  link = select_past.value;
  window.location = link;
}
