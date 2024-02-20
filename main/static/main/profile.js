const data = document.currentScript.dataset;

const user = data.username
const pay = data.pay
const zip = data.pay


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





document.addEventListener("DOMContentLoaded", function(){
	const subjectList = document.getElementById("subject_list");
	subjectList.addEventListener("click", function (event) {
		if (event.target && event.target.classList.contains("rm-sub-button")) {
			const subjectToRemove = event.target.dataset.subject;
			removeSubject(subjectToRemove, user);
		}
	});

	const addSubjectButton = document.querySelector(".add-sub-button");
	if(addSubjectButton)
	{
		addSubjectButton.addEventListener("click", function(){
			newSubject = document.getElementById("new_subject").value.trim();
			const loop = "{{ forloop.counter }}";
			addSubject(newSubject, user, loop);
		});
	}

	function removeSubject(subject, user)
	{
		console.log("Inside removeSubject");
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/remove_subject/${user}/`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		req.onload = function(){
			if (req.status == 200)
			{
				const data = JSON.parse(req.responseText);
				if (data.status === "CONFIRM")
				{
					
					const subjectElement = document.querySelector(`[data-subject="${subject}"]`).closest(".list");
					console.log("subject to remove", subject);
					if (subjectElement) 
					{
                        subjectElement.remove();
						console.log("subject removed");
                    }
					else
					{
						console.error("Failed to remove subject");
					}
				}
				else
				{
					console.error("Failed to remove subject");
				}
			}
		};

		req.send(JSON.stringify({ "subject": subject }));
	}



	function addSubject(newSubject, user, loop)
	{
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/add_subject/${user}/`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		req.onload = function(){
			if (req.status == 200)
			{
				const data = JSON.parse(req.responseText);
				if (data.status === "CONFIRM")
				{
					let newHtml = `<div class="list" id="subject_${loop}">
										<div style="width: 90%;">${newSubject}</div>`;

					if (user) {
						newHtml += `<button id="rm-sub-button" class="rm-sub-button" data-subject="${newSubject}">Remove Subject</button>`;
					}

					newHtml += `</div>`;
					const listContainer = document.getElementById("add_button");

					if (listContainer) 
					{
                        listContainer.insertAdjacentHTML("beforebegin", newHtml);
                        document.getElementById("new_subject").value = "";
                    }
				}
				else
				{
					console.error("Failed to add subject");
				}
			}
			else
			{
				console.error("Failed to add subject");
			}
		};
		req.send(JSON.stringify({ "new_subject": newSubject }));
	}
});



document.addEventListener("DOMContentLoaded", function(){
    const tutoringList = document.getElementById("tutoring_list");
    tutoringList.addEventListener("click", function (event) {
        if (event.target && event.target.classList.contains("rm-tut-button")) {
            const tutoringToRemove = event.target.dataset.tutoring;
            removeTutoring(tutoringToRemove, user);
        }
    });

    const addTutoringButton = document.querySelector(".add-tut-button");
    if(addTutoringButton)
    {
        addTutoringButton.addEventListener("click", function(){
            newTutoringSubject = document.getElementById("new_tutoring").value.trim();
            const loop = "{{ forloop.counter }}";
            addTutoring(newTutoringSubject, user, loop);
        });
    }


	function removeTutoring(tutoring, user)
	{	
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/remove_tutoring/${user}/`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		req.onload = function(){
			console.log("Inside onload");
			if (req.status == 200)
			{
				const data = JSON.parse(req.responseText);
				if (data.status === "CONFIRM")
				{
					console.log("status is CONFIRM");
					const tutoringElement = document.querySelector(`[data-tutoring="${tutoring}"]`).closest(".list");
					console.log("tutoring subject to remove", tutoring);
					if (tutoringElement) 
					{
                        tutoringElement.remove();
                    }
					else
					{
						console.error("Failed to remove subject");
					}
				}
				else
				{
					console.error("Failed to remove subject");
				}
			}
			else
			{
				console.log("request is not 200");
			}
		};

		req.send(JSON.stringify({ "tutoring": tutoring }));
	}



	function addTutoring(newTutoring, user, loop)
	{
		console.log("Adding subject:", newTutoring);
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/add_tutoring/${user}/`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		req.onload = function(){
			if (req.status == 200)
			{
				const data = JSON.parse(req.responseText);
				if (data.status === "CONFIRM")
				{
					let newHtml = `<div class="list" id="tutoring_${loop}">
										<div style="width: 90%;">${newTutoring}</div>`;

					if (user) {
						console.log("Username recognized");
						newHtml += `<button id="rm-sub-button" class="rm-sub-button" data-subject="${newTutoring}">Remove Subject</button>`;
					}

					newHtml += `</div>`;
					const listContainer = document.getElementById("tut_button");

					if (listContainer) 
					{
                        listContainer.insertAdjacentHTML("beforebegin", newHtml);
                        document.getElementById("new_tutoring").value = "";
                    }
				}
				else
				{
					console.error("Failed to add subject");
				}
			}
			else
			{
				console.error("Failed to add subject");
			}
		};
		req.send(JSON.stringify({ "new_tutoring": newTutoring }));
	}
});




function editBio(){
	console.log("editBio function called");
	b2 = document.getElementById("b2");
	bio = document.getElementById("bio");
	bio_text = document.getElementById("bio_text");
  
	bio_textarea = document.createElement("textarea");
	bio_textarea.value = unescapeHTML(bio_text.innerHTML);
	bio_textarea.id = "bio_textarea";
	bio_textarea.setAttribute("maxlength", "500");
	bio_textarea.rows = 5;
	bio.removeChild(bio_text);
	bio.insertBefore(bio_textarea, b2);
	b2.innerHTML = "Save";
	b2.setAttribute("onclick", "saveBio();");
  }


function saveBio(){
	console.log("saveBio function called");
	b2 = document.getElementById("b2");
	bio = document.getElementById("bio");
	bio_textarea = document.getElementById("bio_textarea");

	bio_text = document.createElement("p");
	bio_text.id = "bio_text";
	bio_text.innerHTML = escapeHTML(bio_textarea.value);

	req = new XMLHttpRequest();
	req.open("POST", `/ajax/save_bio/${user}/`);
	req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	req.send(JSON.stringify({"bio": bio_textarea.value}));


	bio.removeChild(bio_textarea);
	bio.insertBefore(bio_text, b2);
	b2.innerHTML = "Edit Bio";
	b2.setAttribute("onclick", "editBio();");
	console.log("AJAX request sent");
}

function saveZip(){
	const zipInput = document.getElementById("zip_code");
	const zip = zipInput.value.trim();


	if(zip.length == 5)
	{
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/save_zip/${user}/`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		const zipCode = document.getElementById("zip_code_display");
		zipCode.textContent = zip;
		zipInput.value = "";
		req.send(JSON.stringify({"zip": zip}));
	}
	else
	{
		console.error("Zip code must be valid");
	}
}

function savePay(){
	const payInput = document.getElementById("tutoring_rate");
	const pay = parseFloat(payInput.value.trim());
	console.log("Pay input: ", pay);


	if(pay)
	{
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/save_pay/${user}/`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		const payRate = document.getElementById("pay_display");
		payRate.innerHTML = `${pay.toFixed(2)}`;
		payInput.value = "";
		req.send(JSON.stringify({"pay": pay}));
	}
	else
	{
		console.error("Pay Rate code cannot be empty");
	}
}

