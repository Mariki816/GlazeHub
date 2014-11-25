$(document).ready(function () {
	var template = $("#compTemplate").clone();
	$("#chem_prcnts_bdy").append(template.children());

	$("#add_component").click(function(e){
		e.preventDefault();
		var template = $("#compTemplate").clone();
		$("#chem_prcnts_bdy").append(template.children());
	});

	$("#getSize").click(function(e){
		e.preventDefault();
		console.log("Button GetSize clicked!");
		var mult = $("#batchsize").val();
		console.log("this is batchsize", mult);
		var amounts = [];
		var numOfChems = (".percentage").length;
		console.log("This is numofchems", numOfChems);
		for (var i = 1; i<=2; i++){

			console.log(($($(".percentage")[i].val()));

			}
	});
});




// onchange select field... get value, user InnerHTML






