#This is my controller script

import model
# import seedchem
from flask import Flask, g, session, render_template, request
from flask import redirect, flash, url_for
import jinja2
import converter
# import os

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnop1234567890'
app.jinja_env.undefined = jinja2.StrictUndefined

# Base.metadata.create_all(engine)

#This is the index page. Later it will show the Calculator itself
@app.route("/")
def index():
	# session["logged_in"] = False
	session["user_id"] =  None
	return render_template("index.html")

#This is the log in page.
@app.route("/login", methods=['GET'])
def showLoginPage():
	session["user_id"] = None
	# print "Init login This is session[user_id]", session["user_id"]
	return render_template("login.html")

def do_login(userID, userEmail):
	session["user"] = userEmail
	session["user_id"] = userID
	pass


#This processes a returning user
@app.route("/process-login", methods = ['POST'])
def processLogin():
	session["user_id"] = None
	# print "This is session[user_id]", session["user_id"]
	email = request.form.get("userEmail")
	pword = request.form.get("password")
	user = model.User.getUserByEmail(email)


	# if pword == pwordcheck:
	if user:
		pwordcheck = model.User.getUserPasswordByEmail(email)
		if pword == pwordcheck:
			flash("Welcome, %s" % (user.user_name))
			if "user" in session:
				session["user_id"] = user.id
			else:
				do_login(user.id, email)
		else:
			flash("Incorrect password. Please try again")
			return render_template("login.html")

	else:
		flash("New User? Please create an account.")
		session["user_id"] = None
		return render_template("login.html")
	return redirect("/userRecipes/%d" % user.id)



#This creates a New user
@app.route("/register", methods =['POST'])
def getNewUser():
	session["user_id"] = None
	newUser = model.User()
	newUser.user_name = request.form.get("NewUserName")
	newUser.email = request.form.get("NewUserEmail")
	newUser.password = request.form.get("NewUserPassword")

	print "This is newUser.email", newUser.email
	model.session.add(newUser)
	model.session.commit()
	session["user_id"] = newUser.id


	flash("Welcome, %s" % (newUser.user_name))
	do_login(newUser.id, newUser.email)
	return redirect("/userRecipes/%d" % newUser.id)


#This is the list of recipes of the logged in user
@app.route("/userRecipes/<int:userViewID>")
def listofUserRecipes(userViewID):
	userLoginID = session["user_id"]
	if userLoginID != userViewID:
		flash ("Invalid User ID. Here are your recipes.")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", display_recipes = recipes)
	else:
		recipes = model.Recipe.getRecipeNamesByUserID(userViewID)
		return render_template("user_recipes.html", display_recipes = recipes)

#This is the function to render the Add Recipe page
@app.route("/addRecipe", methods=['GET'])
def showRecipeAddForm():
	# print "This is ShowRecipeAddForm"
	return render_template("add_recipe.html")


#This function gets the recipe name from the form and adds it to the Recipes table
@app.route("/addRecipe", methods=['POST'])
def addRecipeName():
	# print "This is addRecipeName"
	newRecipe = model.Recipe()
	newRecipe.user_id = session["user_id"]

	newRecipe.recipe_name = request.form.get('recipename')

	model.session.add(newRecipe)
	model.session.commit()

	return redirect("/userRecipes/%d" % newRecipe.user_id)


#this is a tester route
@app.route("/emilysPurpleRecipe")
def emilyspurplerecipe():
	return render_template("emilys_purple_recipe.html")



#this is the recipe page, checks user too
@app.route("/recipecomps/<userViewID>/<recipeName>")
def recipe(userViewID, recipeName):

	userLoginID = session["user_id"]
	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes.")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", display_recipes = recipes)
	else:
		recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
		components = model.Component.getComponentsByRecipeID(recipe.id)
		newComp = []
		return render_template("recipecomps.html", user_id = userViewID, recipe_name = recipeName, components = components, newComp = newComp)


#This function returns the user to the homepage
@app.route("/returnHome")
def returnHome():
	return render_template("index.html")

#This sends you to a way to send a quote to Clay Planet
@app.route("/sendEmailToCP")
def emailCP():
	return render_template("emailCP.html")

@app.route("/batchSizeChange/<userViewID>/<recipeName>",  methods=['POST'])
def batchsizechange(userViewID, recipeName):
	size = request.form.get("batchsize")
	# recipe_name = request.form.get("recipeName")
	print "this is batchsize size", size
	print "this is recipe_name", recipeName
	recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
	print "This is recipe_id", recipe.id
	components = model.Component.getComponentsByRecipeID(recipe.id)
	newComp = []

	for comp in components:
		print "This is comp percentage", comp.percentage
		newComp.append(comp.percentage)

	for i in range(len(newComp)):
		newComp[i] = float(size) * newComp[i]
		print "This is newComp.percentage", newComp[i]
	for comp in components:
		print "This is comp percentage", comp.percentage



	return render_template("recipecomps.html", user_id = userViewID, recipe_name = recipeName, newComp = newComp, components = components)



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



if __name__ == "__main__":
	app.run(debug=True)

