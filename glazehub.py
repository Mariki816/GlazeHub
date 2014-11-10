#This is my controller script

import model
import seedchem
from flask import Flask, g, render_template, request, redirect, flash, url_for
import jinja2

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnop1234567890'
app.jinja_env.undefined = jinja2.StrictUndefined

# Base.metadata.create_all(engine)


@app.route("/")
def index():
    """Return index page."""
    return render_template("index.html")

@app.route("/userRecipes")
def listofUserRecipes():
	# print "This is list of UserRecipes"
	# print "This is g.user", g.user


	recipes = model.getRecipesByUserID(1)
	print "This is recipes", recipes


	return render_template("user_recipes.html", display_recipes = recipes)



@app.route("/addRecipe", methods=['GET'])
def showRecipeAddForm():
	print "This is ShowRecipeAddForm"
	return render_template("add_recipe.html")

@app.route("/addRecipe", methods=['POST'])
def addRecipeName():
	# print "This is addRecipeName"
	newRecipe = model.Recipe()


	newRecipe.recipe_name = request.form.get('recipename')
	newRecipe.user_id = request.form.get('userID')
	print "This is userID", newRecipe.user_id
	if newRecipe.user_id:
		g.user = model.User.query.get(newRecipe.user_id)
		print "This is g", g
		print "This is g.user.id and user_name", g.user.id, g.user.user_name

	else:
		flash("Ooops, issue")
		return redirect("/index")
	model.session.add(newRecipe)
	model.session.commit()

	print newRecipe.recipe_name
	return redirect("/userRecipes")



@app.route("/emilysPurpleRecipe")
def emilyspurplerecipe():
	return render_template("emilys_purple_recipe.html")

@app.route("/returnHome")
def returnHome():
	return render_template("index.html")


@app.route("/sendEmailToCP")
def emailCP():
	return render_template("emailCP.html")

# @app.route("/addComponents")

	#this will work later

	# newComp = model.Component()

	# newComp.chem_id = request.form.get('componentChemID')
	# newComp.percentage = request.form.get('componentPercentage')
	# print "This is: ", newComp.chem_id, newComp.percentage
	# newRecipe.components.append(newComp)






def main():
	pass
	# user_id = 4
	# getUserByID(user_id)
	# getRecipesByUserID(user_id)


if __name__ == "__main__":
	app.run(debug=True)

