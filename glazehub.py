#This is my controller script

import model
import seedchem

# Base.metadata.create_all(engine)

def getUserByID(userID):
	#testing if I can get the user right

	user = model.session.query(model.User).get(userID)
	print user.user_name


def getRecipesByUserID(userID):
	# user = model.session.query(model.User).get(user_id)

	recipenames = model.session.query(model.Recipe).filter_by(user_id=userID).all()

	for rname in recipenames:
		print rname.recipe_name
		getComponentsByRecipeID(rname.id)


def getComponentsByRecipeID(recipeID):
	components = model.session.query(model.Component).filter_by(recipe_id = recipeID).all()

	for comp in components:
		compName = getChemNameByID(comp.chem_id)
		compPercent = comp.percentage
		compChemID= getChemIDbyName(compName)

	return compName, compPercent, compChemID
		# print "This is compChemID", compChemID, compName


def getChemNameByID(chemID):
	chemName = model.session.query(model.Chem).get(chemID).chem_name
	return chemName

def getChemIDbyName(chemNAME):
	chems=model.session.query(model.Chem)
	for c in chems:
		if c.chem_name == chemNAME:
			chemID = c.id

	return chemID



def main():
	user_id = 4
	getUserByID(user_id)
	getRecipesByUserID(user_id)


if __name__ == "__main__":
	main()

