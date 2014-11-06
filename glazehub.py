#This is my controller script

import model
import seedchem
from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnop1234567890'

# Base.metadata.create_all(engine)


@app.route("/")
def index():
    """Return index page."""
    return render_template("recipe.html")

@app.route("/", methods=['POST'])
def addRecipeName():

	newRecipe = model.Recipe()
	# print "This is newRecipe"
	newRecipe.recipe_name = request.form.get('recipename')
	newRecipe.user_id = 1



	# newComp = model.Component()
	# newComp.chem_id = request.form.get('componentChemID')
	# newComp.percentage = request.form.get('componentPercentage')
	# print "This is: ",newComp.chem_id, newComp.percentage
	# newRecipe.components.append(newComp)
	# print "This is chem_id", newRecipe.components[-1].chem_id
	# return newRecipe.recipe_name
	newComp = model.Component()

	newComp.chem_id = request.form.get('componentChemID')
	newComp.percentage = request.form.get('componentPercentage')
	print "This is: ", newComp.chem_id, newComp.percentage
	newRecipe.components.append(newComp)
	newComp.chem_id = request.form.get('componentChemID2')
	newComp.percentage = request.form.get('componentPercentage2')
	newRecipe.components.append(newComp)
	print "This is newRecipe.components", newRecipe.components[0].percentage
	return newRecipe.recipe_name


	# model.session.add(newRecipe)
	# model.session.commit()
	# return "hello"
	# return "This is", newRecipe.recipe_name








def getUserByID(userID):
	#testing if I can get the user right

	user = model.session.query(model.User).get(userID)
	# print user.user_name


def getRecipesByUserID(userID):
	# user = model.session.query(model.User).get(user_id)

	recipenames = model.session.query(model.Recipe).filter_by(user_id=userID).all()

	for rname in recipenames:
		# print rname.recipe_name
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
	app.run(debug=True)

