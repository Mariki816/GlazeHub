#This is my controller script

import model
import seedchem
from flask import Flask, render_template, request, redirect, url_for
import jinja2

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnop1234567890'

# Base.metadata.create_all(engine)


@app.route("/")
def index():
    """Return index page."""
    return render_template("index.html")

@app.route("/addRecipe", methods=['GET'])
def showRecipeAddForm():
	print "This is ShowRecipeAddForm"
	return render_template("add_recipe.html")

@app.route("/addRecipe", methods=['POST'])
def addRecipeName():
	print "This is addRecipeName"
	newRecipe = model.Recipe()
	# print "This is newRecipe"
	newRecipe.recipe_name = request.form.get('recipename')
	newRecipe.user_id = request.form.get('userID')
	model.session.add(newRecipe)
	# model.session.commit()

	print newRecipe.recipe_name
	# newComp = model.Component()

	# newComp.chem_id = request.form.get('componentChemID')
	# newComp.percentage = request.form.get('componentPercentage')
	# print "This is: ", newComp.chem_id, newComp.percentage
	# newRecipe.components.append(newComp)


	return render_template("user_recipes.html")

@app.route("/userRecipes")
def listofUserRecipes():

	return render_template("user_recipes.html")

@app.route("/emilysPurpleRecipe")
def emilyspurplerecipe():
	return render_template("emilys_purple_recipe.html")

@app.route("/returnHome")
def returnHome():
	return redirect(url_for("index"))


@app.route("/sendEmailToCP")
def emailCP():
	return render_template("emailCP.html")

# @app.route("/addComponents")

	#this will work later





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

def getRecipeIDByName(userID, recipename):
	recipes = model.session.query(model.Recipe).filter_by(user_id = userID).all()

	for recipe in recipes:
		if recipes.recipe_name == recipename:
			recipeID = recipes.id

	return recipeID



def main():
	user_id = 4
	getUserByID(user_id)
	getRecipesByUserID(user_id)


if __name__ == "__main__":
	app.run(debug=True)

