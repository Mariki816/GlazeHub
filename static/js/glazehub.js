$(document).ready(function () {
	var template = $("#compTemplate").clone();
	$("#chem_prcnts_bdy").append($("<tr>").append(template.children()));

	$("#add_component").click(function(e){
		e.preventDefault();
		var template = $("#compTemplate").clone();
		$("#chem_prcnts_bdy").append($("<tr>").append(template.children()));

	});



});




// onchange select field... get value,






