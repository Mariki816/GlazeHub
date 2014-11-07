var getChemName = document.getElementById("Chem");


function changeContent(){
	var opt = getChemName.options[0];
	opt.value = 'Zircopax';
	opt.text = 'Zircopax';
	console.log("This is getChemName", opt);
}