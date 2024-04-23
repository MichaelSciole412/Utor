function show_filter()
{
	var filterDisp = document.getElementById("filter-disp");
	if (document.getElementById("filter-type").value !== "no-filter") 
	{
		filterDisp.style.display = "block";
	} 
	else 
	{
		filterDisp.style.display = "none";
	}
}
	
