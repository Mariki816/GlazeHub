$(document).ready(function () {

	$('.delete_comp').click(function(e){
		e.preventDefault();
		console.dir(this);
		$(this.parentElement).remove();
	});

	var template = $("#compTemplate").clone(true);
	$("#chem_prcnts_bdy").append(template.children());


	$("#add_component").click(function(e){
		e.preventDefault();
		var template = $("#compTemplate").clone(true);
		$("#chem_prcnts_bdy").append(template.children());
	});



	$("#getSize").click(function(e){
		e.preventDefault();
		console.log("Button GetSize clicked!");

// Because of hidden template, numOfChems is always one more than what user enters


		var numOfChems = $(".percentage").length;
		console.log("This is numofchems", numOfChems);

		var amount = [];
		var wholeNums = [];
		var leftOverBits = [];
		var leftOverBit = 0;
		var sumOfNums = 0;
		var percent = 0.01;
		var mult = 0;

//hidden template, so starting x at 1

		for (var x = 1; x < numOfChems; x++){
			amount[x] = (($($(".percentage")[x]).val()));
			console.log("this is amount[x]", amount[x]);
			sumOfNums += parseFloat(amount[x]);
			console.log("this is sumOfNums IP", sumOfNums);
		}

		if (sumOfNums != 100){
			var new_percent = 100/sumOfNums;
			percent = 0.01 * new_percent;
			console.log("This is percent", percent);
			$("#messageToUser").html("Recipe does not add up to 100. Amounts adjusted.");
		}


		mult = $("#batchsize").val() * percent;
		console.log("This is mult fixed", mult);


// Starting i with 1 because the first element in numOfChems is 'undefined/nothing'
// because of hidden template
		for (var i = 1; i < numOfChems; i++){
			amount[i] = (($($(".percentage")[i]).val())) * mult;
			wholeNums[i] = Math.floor(amount[i]);


			if ($("input[type='radio'][name='unitSys']:checked").val()=="lbs"){
				leftOverBit = getOunces(amount[i]);
				$($(".amount_needed")[i]).html(wholeNums[i] + "lbs " + leftOverBit + "oz");
			} else{
				leftOverBit = getGrams(amount[i]);
				$($(".amount_needed")[i]).html(wholeNums[i] + "kg " + leftOverBit + "g");

			}
			leftOverBits[i] = leftOverBit;


			}
	});
});






function getOunces(pounds){
	var oz = 0;

	if (pounds >= 1){
		var lbs = Math.floor(pounds);
		var ounces = pounds % lbs;
		oz = Math.round(ounces * 16);
		return oz;

	} else {
		oz = Math.round(pounds*16);
		return oz;

	}
}


function getGrams(kilos){
	var grams = 0;

	if (kilos >=1){
		var kgs = Math.floor(kilos);
		var gms = kilos % kgs;
		grams = Math.round(gms * 1000);
		console.log("This is grams", grams);
		return grams;

	} else {
		grams = Math.round(kilos * 1000);
		console.log("This is grams else", grams);
		return grams;
	}
}


