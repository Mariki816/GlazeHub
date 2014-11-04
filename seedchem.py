# from pprint import pprint
import model
import csv

def load_chems(session):

	with open('chemlist102414.csv', 'rb') as csvfile:
		linereader = csv.reader(csvfile, delimiter = ',')
		chem = model.Chem()
		chem_list = []
		i = 0;
		for row in linereader:
			chem.id = i;
			chem.name = row[0]
			chem.quarter = row[1]
			chem.half = row[2]
			chem.onelb = row[3]
			chem.fivelb = row[4]
			chem.tenlb = row[5]
			chem.twentyfivelb = row[6]
			chem.fiftylb = row[7]
			chem.onehundlb = row[8]
			chem.fivehundlb = row[9]

			i += 1
			chem_list.append(chem.id)

			# print "this is chem", chem.id

	return chem_list



# def getChemById(id):
# 	displaychem = load_chems(session).



def main(session):
# You'll call each of the load_* functions with the session as an argument
	print load_chems(session)
	# print display_chem_id.id
	# pprint (vars(display_chem_id))



# load_ratings(session)
if __name__ == "__main__":
	s= model.connect()
	main(s)