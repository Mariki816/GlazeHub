
$("#add_component").click(function(){

    var objTo = document.getElementById('chems_percents');
    var tablerowtest = document.createElement("tr");
    tablerowtest.innerHTML = '<select name="chem">{% for chem in chem_names %}<option class = "chems" id = "chem" name = "chem" value="{{ chem }}">{{ chem }}</option>{% endfor %}</select>';
    objTo.appendChild(tablerowtest);
}
);





function DropDownTextToBox(objDropdown, strTextboxId) {
	document.getElementById(strTextboxId).value = objDropdown.options[objDropdown.selectedIndex].value;
	DropDownIndexClear(objDropdown.id);
document.getElementById(strTextboxId).focus();
}

function DropDownIndexClear(strDropdownId) {
	if (document.getElementById(strDropdownId) !== null) {
		document.getElementById(strDropdownId).selectedIndex = -1;
	}
}