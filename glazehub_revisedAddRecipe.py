#This is my controller script

import model
# import seedchem
from flask import Flask, g, session, render_template, request, redirect, flash, url_for
import jinja2
import os

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnop1234567890'
app.jinja_env.undefined = jinja2.StrictUndefined

# Base.metadata.create_all(engine)

#This is the index page. Later it will show the Calculator itself
@app.route("/")
def index():
    """Return index page."""
    return render_template("index.html")


#This is the list of recipes of the logged in user
@app.route("/userRecipes")
def listofUserRecipes():
	# print "This is list of UserRecipes"
	# print "This is g.user", g.user


	recipes = model.getRecipesByUserID(1)
	print "This is recipes", recipes


	return render_template("user_recipes.html", display_recipes = recipes)

#This is the log in page.
@app.route("/login", methods=['GET'])
def showLoginPage():
	return render_template("login.html")

@app.route("/login", methods = ['POST'])
def processLogin():
	session["logged_in"] = False
	email = request.form.get("email")
	user = model.getUserByEmail(email)

	if user:
		flash ("Welcome, %s" % (user.user_name))
		if "user" in session:
			session ["logged_in"] = True
		else:
			session["user"] = email
			session["logged_in"] = True
		return redirect("/index")
	else:
		flash("New User? Please create an account.")
		session["logged_in"] = False
		return render_template("login.html")



#This is the function to render the Add Recipe page
@app.route("/addRecipe", methods=['GET'])
def showRecipeAddForm():
	# print "This is ShowRecipeAddForm"
	return render_template("add_recipe.html")


#This function gets the recipe name from the form and adds it to the Recipes table
@app.route("/addRecipe/<int:userID>", methods=['POST'])
def addRecipeName(userID):
	# print "This is addRecipeName"
	newRecipe = model.Recipe()


	newRecipe.recipe_name = request.form.get('recipename')
	newRecipe.user_id = userID
	# print "This is userID", newRecipe.user_id
	# if newRecipe.user_id:
	# 	g.user = model.User.query.get(newRecipe.user_id)
	# 	print "This is g", g
	# 	print "This is g.user.id and user_name", g.user.id, g.user.user_name

	# else:
	# 	flash("Ooops, issue")
	# 	return redirect("/index")
	model.session.add(newRecipe)
	model.session.commit()

	print newRecipe.recipe_name
	return redirect("/userRecipes")


#this it a tester route
@app.route("/emilysPurpleRecipe")
def emilyspurplerecipe():
	return render_template("emilys_purple_recipe.html")


#This function returns the user to the homepage
@app.route("/returnHome")
def returnHome():
	return render_template("index.html")

#This sends you to a way to send a quote to Clay Planet
@app.route("/sendEmailToCP")
def emailCP():
	return render_template("emailCP.html")


#Will add components to the recipe
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

