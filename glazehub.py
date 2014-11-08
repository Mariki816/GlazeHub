#This is my controller script

import model
import seedchem
from flask import Flask, render_template, request, redirect, url_for
import jinja2

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnop1234567890'
app.jinja_env.undefined = jinja2.StrictUndefined

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
	recipes = model.session["userRecipes"]
	dict_of_recipes = {}

	for recipe in recipes:
		dict_of_recipes[recipe.recipe_name] = {"user_id":4, "recipe_name":recipe.recipe_name}

	return render_template("user_recipes.html", display_recipes = dict_of_recipes)


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








def main():
	user_id = 4
	getUserByID(user_id)
	getRecipesByUserID(user_id)


if __name__ == "__main__":
	app.run(debug=True)

