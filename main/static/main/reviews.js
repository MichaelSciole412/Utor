const data = document.currentScript.dataset;

const user = data.username;
const tutor = data.tutorname;
const overall = data.overall;
const effective = data.effective;
const knowledge = data.knowledge;
const timeliness = data.timeliness;
const patience = data.patience;


for(let i = 1; i <= overall; i++)
{
	document.getElementById("overall_rate_" + i.toString()).classList.add('selected');
}

for(let i = 1; i <= effective; i++)
{
	document.getElementById("effective_rate_" + i.toString()).classList.add('selected');
}

for(let i = 1; i <= timeliness; i++)
{
	document.getElementById("timeliness_rate_" + i.toString()).classList.add('selected');
}

for(let i = 1; i <= knowledge; i++)
{
	document.getElementById("knowledge_rate_" + i.toString()).classList.add('selected');
}

for(let i = 1; i <= patience; i++)
{
	document.getElementById("patience_rate_" + i.toString()).classList.add('selected');
}

const overallRate = document.querySelectorAll(".overall_rating");
overallRate.forEach((span, index) => {
	span.addEventListener('click', function() {
		overallRate.forEach((s,i) => {
			if (i < index)
			{
				s.classList.remove('selected');
			}
			else
			{
				s.classList.add('selected');
			}
		});
		console.log(this.id);
		setOverall(this.id);
	});
});

const effectiveRate = document.querySelectorAll(".effective_rating");
effectiveRate.forEach((span, index) => {
	span.addEventListener('click', function() {
		effectiveRate.forEach((s,i) => {
			if (i < index)
			{
				s.classList.remove('selected');
			}
			else
			{
				s.classList.add('selected');
			}
		});
		console.log(this.id);
		setEffective(this.id);
	});
});

const timeRate = document.querySelectorAll(".timeliness_rating");
timeRate.forEach((span, index) => {
	span.addEventListener('click', function() {
		timeRate.forEach((s,i) => {
			if (i < index)
			{
				s.classList.remove('selected');
			}
			else
			{
				s.classList.add('selected');
			}
		});
		console.log(this.id);
		setTime(this.id);
	});
});

const patienceRate = document.querySelectorAll(".patience_rating");
patienceRate.forEach((span, index) => {
	span.addEventListener('click', function() {
		patienceRate.forEach((s,i) => {
			if (i < index)
			{
				s.classList.remove('selected');
			}
			else
			{
				s.classList.add('selected');
			}
		});
		this.classList.add('selected');
		console.log(this.id);
		setPatience(this.id);
	});
});

const knowledgeRate = document.querySelectorAll(".knowledge_rating");
knowledgeRate.forEach((span, index) => {
	span.addEventListener('click', function() {
		knowledgeRate.forEach((s,i) => {
			if (i < index)
			{
				s.classList.remove('selected');
			}
			else
			{
				s.classList.add('selected');
			}
		});
		this.classList.add('selected');
		console.log(this.id);
		setKnowledge(this.id);
	});
});

function setOverall(ratingId)
{
	let overall;
	if (ratingId != '')
	{
		console.log("Creating request");
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/setOverall/${tutor}`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		if (ratingId == 'overall_rate_1')
		{
			overall = 1;
		}
		else if (ratingId == 'overall_rate_2')
		{
			overall = 2;
		}
		else if (ratingId == 'overall_rate_3')
		{
			overall = 3;
		}
		else if (ratingId == 'overall_rate_4')
		{
			overall = 4;
		}
		else if (ratingId == 'overall_rate_5')
		{
			overall = 5;
		}
		else
		{
			overall = 0;
		}

		req.send(JSON.stringify({"overall": overall}));

	}
}


function setEffective(ratingId)
{
	let effective;
	if (ratingId != '')
	{
		console.log("Creating request");
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/setEffective/${tutor}`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		if (ratingId == 'effective_rate_1')
		{
			effective = 1;
		}
		else if (ratingId == 'effective_rate_2')
		{
			effective = 2;
		}
		else if (ratingId == 'effective_rate_3')
		{
			effective = 3;
		}
		else if (ratingId == 'effective_rate_4')
		{
			effective = 4;
		}
		else if (ratingId == 'effective_rate_5')
		{
			effective = 5;
		}
		else
		{
			effective = 0;
		}

		req.send(JSON.stringify({"effective": effective}));
	}
}

function setTime(ratingId)
{
	let timeliness;
	if (ratingId != '')
	{
		console.log("Creating request");
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/setTime/${tutor}`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		if (ratingId == 'timeliness_rate_1')
		{
			timeliness = 1;
		}
		else if (ratingId == 'timeliness_rate_2')
		{
			timeliness = 2;
		}
		else if (ratingId == 'timeliness_rate_3')
		{
			timeliness = 3;
		}
		else if (ratingId == 'timeliness_rate_4')
		{
			timeliness = 4;
		}
		else if (ratingId == 'timeliness_rate_5')
		{
			timeliness = 5;
		}
		else
		{
			timeliness = 0;
		}

		req.send(JSON.stringify({"timeliness": timeliness}));
	}
}

function setPatience(ratingId)
{
	let patience;
	if (ratingId != '')
	{
		console.log("Creating request");
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/setPatience/${tutor}`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		if (ratingId == 'patience_rate_1')
		{
			patience = 1;
		}
		else if (ratingId == 'patience_rate_2')
		{
			patience = 2;
		}
		else if (ratingId == 'patience_rate_3')
		{
			patience = 3;
		}
		else if (ratingId == 'patience_rate_4')
		{
			patience = 4;
		}
		else if (ratingId == 'patience_rate_5')
		{
			patience = 5;
		}
		else
		{
			patience = 0;
		}

		req.send(JSON.stringify({"patience": patience}));
	}
}

function setKnowledge(ratingId)
{
	let knowledge;
	if (ratingId != '')
	{
		console.log("Creating request");
		req = new XMLHttpRequest();
		req.open("POST", `/ajax/setKnowledge/${tutor}`);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

		if (ratingId == 'knowledge_rate_1')
		{
			knowledge = 1;
		}
		else if (ratingId == 'knowledge_rate_2')
		{
			knowledge = 2;
		}
		else if (ratingId == 'knowledge_rate_3')
		{
			knowledge = 3;
		}
		else if (ratingId == 'knowledge_rate_4')
		{
			knowledge = 4;
		}
		else if (ratingId == 'knowledge_rate_5')
		{
			knowledge = 5;
		}
		else
		{
			knowledge = 0;
		}

		req.send(JSON.stringify({"knowledge": knowledge}));
	}
}