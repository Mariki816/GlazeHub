#This is my controller script

import model
# import seedchem
from flask import Flask, g, session, render_template, request
from flask import redirect, flash, url_for
import jinja2
import os

app = Flask(__name__)

app.secret_key = 'abcdefghijklmnop1234567890'
app.jinja_env.undefined = jinja2.StrictUndefined

# Base.metadata.create_all(engine)

#This is the index page. Later it will show the Calculator itself
@app.route("/")
def index():
	session["logged_in"] = False
	return render_template("index.html")

#This is the log in page.
@app.route("/login", methods=['GET'])
def showLoginPage():
	session["logged_in"] = False
	return render_template("login.html")


#This processes a returning user
@app.route("/process-login", methods = ['POST'])
def processLogin():
	session["logged_in"] = False
	email = request.form.get("userEmail")
	do_login(userEmail)



def do_login(userEmail):
	user = model.User.getUserByEmail(email)
	# Find the commonalities of the new user and returning user
	# maybe just add only the session stuff...
	# user = model.session.query(model.User).filter_by(email=email).first()
	# user_id = model.getUserIDByEmail(email)

	# user = model.session.query(model.User).get(user_id)

	if user:
		flash("Welcome, %s" % (user.user_name))
		if "user" in session:
			session ["logged_in"] = True
		else:
			session["user"] = email
			session["logged_in"] = True

	else:
		flash("New User? Please create an account.")
		session["logged_in"] = False
		return render_template("login.html")

#This creates a New user
@app.route("/register", methods =['POST'])
def getNewUser():
	session["logged_in"] = False
	newUser = model.User()
	newUser.user_name = request.form.get("NewUserName")
	newUser.email = request.form.get("NewUserEmail")
	newUser.password = "password"

	print "This is newUser.email", newUser.email
	model.session.add(newUser)
	model.session.commit()
	return "Registered"



#This is the list of recipes of the logged in user
@app.route("/userRecipes/<int:userID>")
def listofUserRecipes(userID):
	recipes = model.getRecipesByUserID(userID)
	return render_template("user_recipes.html", display_recipes = recipes)

#This is the function to render the Add Recipe page
@app.route("/addRecipe", methods=['GET'])
def showRecipeAddForm():
	# print "This is ShowRecipeAddForm"
	return render_template("add_recipe.html")


#This function gets the recipe name from the form and adds it to the Recipes table
@app.route("/addRecipe", methods=['POST'])
def addRecipeName(userID):
	# print "This is addRecipeName"
	newRecipe = model.Recipe()
	newRecipe.user_id = userID

	newRecipe.recipe_name = request.form.get('recipename')

	model.session.add(newRecipe)
	model.session.commit()

	return redirect("/userRecipes/%d" % newRecipe.user_id)


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

