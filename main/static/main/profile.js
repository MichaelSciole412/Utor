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
	const pay = payInput.value.trim();


	if(pay)
	{
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/save_pay/${user}/`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		const payRate = document.getElementById("pay_display");
		payRate.textContent = pay;
		payInput.value = "";
		req.send(JSON.stringify({"pay": pay}));
	}
	else
	{
		console.error("Pay Rate code cannot be empty");
	}
}

