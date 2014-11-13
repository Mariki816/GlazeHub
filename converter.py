def kiloToPounds(kilos):
	pounds = kilos*2.20462
	return pounds



def leftOverPoundsToOunces(pounds):
	lbs = int(pounds)
	ounces = pounds % lbs
	oz = int(ounces * 16)
	return oz


def leftOverKilosToGrams(kilos):
	kgs = int(kilos)
	gs = kilos % kgs
	grams = int(gs * 1000)
	return grams

def mult(percentage, batch_size):
	result = percentage * batch_size
	return result





def main():
	pass





if __name__ == "__main__":

	main()