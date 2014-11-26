#This is my controller script

import model
# import seedchem
from flask import Flask, session, render_template, request
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
	session["user_id"] =  None
	return render_template("index.html")

@app.route("/logout", methods = ['GET'])
def Logout():

	session.clear()

	return redirect("/")


#This is the log in page.
@app.route("/login", methods=['GET'])
def showLoginPage():
	session["user_id"] = None
	return render_template("login.html")


def do_login(userID, userEmail, userName):
	session["user"] = userEmail
	session["user_id"] = userID
	session["user_name"] = userName
	return


#This processes a returning user
@app.route("/process-login", methods = ['POST'])
def processLogin():
	session["user_id"] = None
	session["user_name"] = None

	email = request.form.get("userEmail")
	pword = request.form.get("password")
	user = model.User.getUserByEmail(email)


	if user:
		pwordcheck = model.User.getUserPasswordByEmail(email)
		if pword == pwordcheck:
			flash("Welcome, %s" % (user.user_name))
		# if the user is already logged in do the first part
			if "user" in session:
				session["user_id"] = user.id
				session["user_name"] = user.user_name
				# print "This is username", session["user_name"]

			else:
				do_login(user.id, email, user.user_name)
		else:
			flash("Incorrect password. Please try again")
			return render_template("login.html")

	else:
		flash("New User? Please create an account.")
		session["user_id"] = None
		session["user_name"] = None
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

	flash("Welcome, %s" % (newUser.user_name))
	do_login(newUser.id, newUser.email, newUser.user_name)
	return redirect("/userRecipes/%d" % newUser.id)


#This is the list of recipes of the logged in user
@app.route("/userRecipes/<int:userViewID>")
def listofUserRecipes(userViewID):
	userLoginID = session["user_id"]
	# print "This is userViewID", userViewID
	# print "This is userLoginID", (type(userLoginID), userLoginID)

	lbschecked = ""
	kgchecked = 'checked = "checked"'

	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes.4")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", display_recipes = recipes, user_id = userViewID,
			kgchecked = kgchecked, lbschecked=lbschecked)
	else:
		recipes = model.Recipe.getRecipeNamesByUserID(userViewID)
		return render_template("user_recipes.html", display_recipes = recipes,
			lbschecked = lbschecked, kgchecked = kgchecked, user_id = userViewID)


def showUserRecipeList(userViewID):
	userLoginID = session["user_id"]
	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes. 3")
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
	components = model.Component()
	if "user_id" in session:
		user_id = session["user_id"]
	else:
		user_id = None

	lbschecked = ""
	kgchecked = 'checked = "checked"'
	wholenumlist=[]
	leftoverbitslist =[]
	messageToUser = ""
	batchsize = 0.0
	recipename = ""
	percentage = 0.0
	session["chem"] = ""
	session["percentage"] =0.0

	return render_template("enter_recipe.html", chem_names = chemNames,\
		batchComp = batchComp, user_id = user_id, lbschecked=lbschecked,
		kgchecked=kgchecked, wholenumlist=wholenumlist, leftoverbitslist = leftoverbitslist,
		chem_list = chems, messageToUser = messageToUser, components = components,\
		batchsize=batchsize, recipename = recipename, percentage = percentage)



#This is the function to calculate on the Enter Recipe page if not logged in
@app.route("/enterRecipe", methods=['POST'])
def enterRecipe():

	recipeName = request.form.get('recipename')
	batchsize = request.form.get('batchsize')


	newRecipe = model.Recipe()
	newRecipe.recipe_name = recipeName


	batchComp=[]
	sizeflt = float(batchsize)
	kgchecked = 'checked = "checked"'
	lbschecked = ""
	unitSys = "kg"
	percent_list = []
	wholenumlist = []
	leftoverbitslist = []
	messageToUser = None

	chem_list=request.values.getlist('chem')
	percentages=request.values.getlist('percentage')
	if percentages == []:
		flash ("no entry")
		return redirect ("/enterRecipe")

	i = 0
	for chem in chem_list:
		comp = model.Component()
		comp.chem_name = chem
		comp.chem_id = model.Chem.getChemIDByName(comp.chem_name)
		comp.percentage = float(percentages[i])
		percent_list.append(comp.percentage)
		i += 1
		comp.recipe_id = newRecipe.id
		batchComp.append(float(comp.percentage))


	onehundred = converter.checkPercent(percent_list)
	newPercent = converter.getPercentMult(percent_list)

	if onehundred == False:
		messageToUser = "Recipe does not add up to 100. Amounts adjusted."
	else:
		messageToUser = None

	for i in range(len(batchComp)):
		batchComp[i] = (sizeflt * batchComp[i])*newPercent

		wholenumlist.append(int(batchComp[i]))
		if unitSys == "kg":
			leftoverbitslist.append(int(converter.leftOverKilosToGrams(batchComp[i])))
			kgchecked = 'checked = "checked"'
		else:
			leftoverbitslist.append(int(converter.leftOverPoundsToOunces(batchComp[i])))
			lbschecked = 'checked = "checked"'


	return render_template("calc_recipe.html", recipe_name = newRecipe.recipe_name,\
			chem_list = chem_list, percentages = percentages, batchComp = batchComp,\
			batchsize = batchsize, kgchecked = kgchecked, lbschecked = lbschecked,\
			unitSys = unitSys, wholenumlist = wholenumlist, leftoverbitslist = leftoverbitslist,\
			messageToUser = messageToUser)




#This is the function to render the Add Recipe page if logged in
@app.route("/addRecipe/<int:userViewID>", methods=['GET'])
def showRecipeAddForm(userViewID):

	userLoginID = session["user_id"]
	recipe_name = ""

	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes. 2")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", user_id = userViewID, display_recipes = recipes)
	else:
		display_recipes = showUserRecipeList(userViewID)
		chems = model.session.query(model.Chem).all()
		chemNames = [chem.chem_name for chem in chems]
		components = []


	return render_template("add_recipe.html", chem_names = chemNames, user_id = userViewID,
			display_recipes= display_recipes, recipe_name = recipe_name, components = components)





#This function gets the recipe name from the form and adds it to the Recipes table
@app.route("/addRecipe/<int:userViewID>", methods=['POST'])
def addRecipe(userViewID):

	display_recipes = showUserRecipeList(userViewID)
	recipe_name = request.form.get('recipename')
	notes = request.form.get('usercomments')

	dupe = model.session.query(model.Recipe).filter_by(recipe_name = recipe_name)\
	.filter_by(user_id = session["user_id"]).all()

	if dupe != []:
		flash("Duplicate Recipe Name")
		return redirect ("/addRecipe/" + str(userViewID))

	newRecipe = model.Recipe()
	newRecipe.user_id = session["user_id"]
	newRecipe.recipe_name = recipe_name
	newRecipe.user_notes = notes

	display_recipes.append(newRecipe)

	model.session.add(newRecipe)
	model.session.commit()



	batchComp=[]
	batchsize = None
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

	kgchecked = 'checked = "checked"'
	lbschecked = ""
	unitSys = "kg"
	wholenumlist = []
	leftoverbitslist = []
	messageToUser = None


	components = model.Component.getComponentsByRecipeID(newRecipe.id)
	print "this is components type", type(components)


	return render_template("recipecomps.html", user_id = userViewID, recipe_name = newRecipe.recipe_name,\
			components = components, batchComp = batchComp, batchsize = batchsize, display_recipes = display_recipes,\
			user_notes = newRecipe.user_notes, kgchecked = kgchecked, lbschecked = lbschecked,
			unitSys = unitSys, wholenumlist = wholenumlist, leftoverbitslist = leftoverbitslist,\
			messageToUser = messageToUser)







#this is the recipe page, checks user too
@app.route("/recipecomps/<userViewID>/<recipeName>")
def recipe(userViewID, recipeName):

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


	messageToUser = None

	batchComp = []
	wholenumlist = []
	leftoverbitslist = []
	batchsize = None

	unit_sys = "unitSys"
	lbschecked = ""
	kgchecked = 'checked = "checked"'

	return render_template("/recipecomps.html/", user_id = userViewID, recipe_name = recipeName,
			components = components, batchComp = batchComp, display_recipes=display_recipes,
			user_notes = recipe.user_notes, messageToUser = messageToUser, unitSys = unit_sys,
			batchsize = batchsize, wholenumlist=wholenumlist, lbschecked =lbschecked,
			kgchecked =kgchecked, leftoverbitslist=leftoverbitslist)


@app.route("/batchSizeChange/<userViewID>/<recipeName>",  methods=['POST'])
def batchSizeChange(userViewID, recipeName):
	display_recipes = showUserRecipeList(userViewID)
	size = request.form.get("batchsize")
	units = request.form.get("unitSys")


	recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
	components = model.Component.getComponentsByRecipeID(recipe.id)
	batchComp = []

	percent_list = []
	for comp in components:
		percent_list.append(comp.percentage)

	onehundred = converter.checkPercent(percent_list)
	newPercent = converter.getPercentMult(percent_list)


	if onehundred == False:
		messageToUser = "Recipe does not add up to 100. Amount adjusted."
	else:
		messageToUser = None

	for comp in components:
		batchComp.append(comp.percentage/100)
	sizeflt = float(size)
	wholenumlist = []
	leftoverbitslist = []
	kgchecked = ""
	lbschecked = ""

	for i in range(len(batchComp)):
		batchComp[i] = (sizeflt * batchComp[i])*newPercent

		wholenumlist.append(int(batchComp[i]))
		if units == "kg":
			leftoverbitslist.append(int(converter.leftOverKilosToGrams(batchComp[i])))
			kgchecked = 'checked = "checked"'
		else:
			leftoverbitslist.append(int(converter.leftOverPoundsToOunces(batchComp[i])))
			lbschecked = 'checked = "checked"'





	return render_template("recipecomps.html", user_id = userViewID, recipe_name = recipeName,
		batchComp = batchComp, components = components, display_recipes=display_recipes,
		user_notes = recipe.user_notes, messageToUser = messageToUser, batchsize = size,
		wholenumlist = wholenumlist, leftoverbitslist = leftoverbitslist, kgchecked = kgchecked,
		lbschecked = lbschecked, unitSys = units)


@app.route("/editRecipe/<userViewID>/<recipeName>", methods=['GET'])
def showEditRecipeForm(userViewID, recipeName):

	userLoginID = session["user_id"]
	recipe_name = recipeName

	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes. 2")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", user_id = userViewID, display_recipes = recipes)
	else:
		display_recipes = showUserRecipeList(userViewID)
		chems = model.session.query(model.Chem).all()
		chemNames = [chem.chem_name for chem in chems]
		recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
		components = model.Component.getComponentsByRecipeID(recipe.id)
		user_notes = recipe.user_notes

		for comp in components:
			print "This is comp.chem.chem_name", comp.chem.chem_name

		print "user_notes", user_notes


	return render_template("edit_recipe.html", chem_names = chemNames, user_id = userViewID,
			display_recipes= display_recipes, recipe_name = recipe_name, components = components,\
			user_notes = user_notes)



@app.route("/editRecipe/<userViewID>/<recipeName>", methods=['POST'])
def updateRecipe(userViewID, recipeName):

	userLoginID = session["user_id"]
	recipe_name = recipeName

	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes. 2")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", user_id = userViewID, display_recipes = recipes)
	else:
		display_recipes = showUserRecipeList(userViewID)
		chems = model.session.query(model.Chem).all()
		chemNames = [chem.chem_name for chem in chems]
		recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
		components = recipe.components
		user_notes = recipe.user_notes

		for comp in components:
			print "This is comp.chem.chem_name", comp.chem.chem_name

		print "user_notes", user_notes


	return render_template("edit_recipe.html", chem_names = chemNames, user_id = userViewID,
			display_recipes= display_recipes, recipe_name = recipe_name, components = components,\
			user_notes = user_notes)



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

