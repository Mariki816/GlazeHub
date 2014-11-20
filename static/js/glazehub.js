$(document).ready(function () {
	$("#add_component").click(add_field);
});
var counter = 0;
function add_field(){
	console.log("I am in addComponent");
    var objTo = document.getElementById('chems_percents');
    var tablerow = document.createElement("tr");

    var tabledata1 = document.createElement("td");
    var tabledata2 = document.createElement("td");

    tabledata1.innerHTML = '<input class = "form-control" name="inputChemName" type="text"" id="inputChemName";" /><select name="chem">{% for chem in chem_names %}<option class = "chems" id = "chem" name = "chem" value="$chem">$chem</option>{% endfor %}</select>';
	objTo.appendChild(tabledata1);
    tabledata2.innerHTML = '<input class = "form-control" type = "text" id = "percentage1" name="percentage1"/>';
    objTo.appendChild(tabledata2);
    objTo.appendChild(tablerow);
    counter ++;
}






function DropDownTextToBox(objDropdown, strTextboxId) {
	document.getElementById(strTextboxId).value = objDropdown.options[objDropdown.selectedIndex].value;
	DropDownIndexClear(objDropdown.id);
document.getElementById(strTextboxId).focus();
}

function DropDownIndexClear(strDropdownId) {
	if (document.getElementById(strDropdownId) !== null) {
		document.getElementById(strDropdownId).selectedIndex = document.getElementById(strDropdownId).selectedIndex;
	}
}


