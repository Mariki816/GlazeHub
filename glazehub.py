#This is my controller script

import model
import api
# import seedchem
from flask import Flask, g, session, render_template, request
from flask import redirect, flash, url_for
import jinja2
import converter
import json

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
	# print "This is user.id", (user.id, user.user_name)

	# if pword == pwordcheck:
	if user:
		pwordcheck = model.User.getUserPasswordByEmail(email)
		if pword == pwordcheck:
			flash("Welcome, %s" % (user.user_name))
			if "user" in session:
				session["user_id"] = user.id
				# print "this is session user", session["user_id"]

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
	# print "This is userViewID", userViewID
	# print "This is userLoginID", (type(userLoginID), userLoginID)
	if userLoginID != userViewID:
		flash ("Invalid User ID. Here are your recipes.")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", display_recipes = recipes, user_id = userViewID)
	else:
		recipes = model.Recipe.getRecipeNamesByUserID(userViewID)
		return render_template("user_recipes.html", display_recipes = recipes, user_id = userViewID)


def showUserRecipeList(userViewID):
	userLoginID = session["user_id"]
	if userLoginID != userViewID:
		flash ("Invalid User ID. Here are your recipes.")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return recipes
	else:
		recipes = model.Recipe.getRecipeNamesByUserID(userViewID)
		return recipes




#This is the function to render the Enter Recipe page if not logged in
@app.route("/enterRecipe", methods=['GET'])
def renderEnterRecipeForm():

	chems = model.session.query(model.Chem).all()
	chemNames = [chem.chem_name for chem in chems]
	batchComp = []

	return render_template("enter_recipe.html", chem_names = chemNames, batchComp = batchComp)



#This is the function to calculate on the Enter Recipe page if not logged in
@app.route("/batchSizeChangeNoUser", methods=['POST'])
def EnterRecipeForm():

	chems = model.session.query(model.Chem).all()
	chemNames = [chem.chem_name for chem in chems]

	size = request.form.get("batchsize")
	sizeflt = float(size)
	# print "this is sizeflt", sizeflt
	batchComp = []



	recipe = model.Recipe()
	recipe.recipe_name = request.form.get('recipename')


	comp1 = model.Component()

	comp1.chem_name = request.form.get('chem1')
	comp1.chem_id = model.Chem.getChemIDByName(comp1.chem_name)
	comp1.percentage = request.form.get('percentage1')
	comp1.recipe_id = recipe.id
	batchComp.append(float(comp1.percentage))


	for i in range(len(batchComp)):
		print "This is batchComp[i]",batchComp[i]
		print "this is type", type(batchComp[i])
		batchComp[i] = sizeflt * batchComp[i]





	return render_template("enter_recipe.html", chem_names = chemNames, batchComp = batchComp)



#This is the function to render the Add Recipe page if logged in
@app.route("/addRecipe/<userViewID>", methods=['GET'])
def showRecipeAddForm(userViewID):

	userLoginID = session["user_id"]
	# print "This is user LoginID", userLoginID
	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes.")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", display_recipes = recipes)
	else:
		display_recipes = showUserRecipeList(userViewID)
		chems = model.session.query(model.Chem).all()
		chemNames = [chem.chem_name for chem in chems]

	return render_template("add_recipe.html", chem_names = chemNames, user_id = userViewID,
			display_recipes= display_recipes)





#This function gets the recipe name from the form and adds it to the Recipes table
@app.route("/addRecipe/<userViewID>", methods=['POST'])
def addRecipeName(userViewID):

	display_recipes = showUserRecipeList(userViewID)

	newRecipe = model.Recipe()
	newRecipe.user_id = session["user_id"]
	newRecipe.recipe_name = request.form.get('recipename')
	newRecipe.user_notes = request.form.get('usercomments')
	model.session.add(newRecipe)
	model.session.commit()

	batchComp=[]
	chem_list=request.values.getlist('chem')
	percentages=request.values.getlist('percentage')
	i = 0
	for chem in chem_list:
		comp = model.Component()
		comp.chem_name = chem
		comp.chem_id = model.Chem.getChemIDByName(comp.chem_name)
		comp.percentage = float(percentages[i])
		i += 1
		comp.recipe_id = newRecipe.id
		batchComp.append(float(comp.percentage))
		model.session.add(comp)
		model.session.commit()


	components = model.Component.getComponentsByRecipeID(newRecipe.id)

	return render_template("recipecomps.html", user_id = userViewID, recipe_name = newRecipe.recipe_name,
			components = components, batchComp = batchComp, display_recipes = display_recipes,
			user_notes = newRecipe.user_notes)







#this is the recipe page, checks user too
@app.route("/recipecomps/<userViewID>/<recipeName>")
def recipe(userViewID, recipeName):
	print "this is recipecomps UserViewID", userViewID
	display_recipes = showUserRecipeList(userViewID)

	userLoginID = session["user_id"]
	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes.")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", display_recipes = recipes)
	else:
		recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
		components = model.Component.getComponentsByRecipeID(recipe.id)
		batchComp = []
		for comp in components:
			batchComp.append(comp.percentage/100)
		return render_template("recipecomps.html", user_id = userViewID, recipe_name = recipeName,
			components = components, batchComp = batchComp, display_recipes=display_recipes, user_notes = recipe.user_notes)



@app.route("/batchSizeChange/<userViewID>/<recipeName>",  methods=['POST'])
def batchsizechange(userViewID, recipeName):
	display_recipes = showUserRecipeList(userViewID)
	size = request.form.get("batchsize")
	# recipe_name = request.form.get("recipeName")
	print "this is batchsize size", size
	print "this is recipe_name", recipeName
	recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
	print "This is recipe_id", recipe.id
	components = model.Component.getComponentsByRecipeID(recipe.id)
	batchComp = []

	for comp in components:
		# print "This is comp percentage", comp.percentage
		batchComp.append(comp.percentage/100)
	sizeflt = float(size)
	print "sizeflt type", type(sizeflt)
	for i in range(len(batchComp)):
		batchComp[i] = sizeflt * batchComp[i]
	# 	print "This is newComp.percentage", newComp[i]
	# for comp in components:
	# 	print "This is comp percentage", comp.percentage

	return render_template("recipecomps.html", user_id = userViewID, recipe_name = recipeName,
		batchComp = batchComp, components = components, display_recipes=display_recipes,
		user_notes = recipe.user_notes)






#This function returns the user to the homepage
@app.route("/returnHome")
def returnHome():
	return render_template("index.html")

#This sends you to a way to send a quote to Clay Planet
@app.route("/sendEmailToCP")
def emailCP():
	return render_template("emailCP.html")



def listChemNames():
	chems = model.session.query(model.Chem).all()
	chemicalNames = [chem.chem_name for chem in chems]
	return chemicalNames







def main():
	pass



if __name__ == "__main__":
	app.run(debug=True)

