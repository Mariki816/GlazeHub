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

@app.route("/base2")
def testBS():
	return render_template("base2.html")

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


	comp2 = model.Component()
	comp2.chem_name = request.form.get('chem2')
	comp2.chem_id = model.Chem.getChemIDByName(comp2.chem_name)
	comp2.percentage = request.form.get('percentage2')
	comp2.recipe_id = recipe.id
	batchComp.append(float(comp2.percentage))

	comp3 = model.Component()
	comp3.chem_name = request.form.get('chem3')
	comp3.chem_id = model.Chem.getChemIDByName(comp3.chem_name)
	comp3.percentage = request.form.get('percentage3')
	comp3.recipe_id = recipe.id
	batchComp.append(float(comp3.percentage))


	comp4 = model.Component()
	comp4.chem_name = request.form.get('chem4')
	comp4.chem_id = model.Chem.getChemIDByName(comp4.chem_name)
	comp4.percentage = request.form.get('percentage4')
	comp4.recipe_id = recipe.id
	batchComp.append(float(comp4.percentage))


	comp5 = model.Component()
	comp5.chem_name = request.form.get('chem5')
	comp5.chem_id = model.Chem.getChemIDByName(comp5.chem_name)
	comp5.percentage = request.form.get('percentage5')
	comp5.recipe_id = recipe.id
	batchComp.append(float(comp5.percentage))


	comp6 = model.Component()
	comp6.chem_name = request.form.get('chem6')
	comp6.chem_id = model.Chem.getChemIDByName(comp6.chem_name)
	comp6.percentage = request.form.get('percentage6')
	comp6.recipe_id = recipe.id
	batchComp.append(float(comp6.percentage))

	for i in range(len(batchComp)):
		print "This is batchComp[i]",batchComp[i]
		print "this is type", type(batchComp[i])
		batchComp[i] = sizeflt * batchComp[i]





	return render_template("enter_recipe.html", chem_names = chemNames, batchComp = batchComp)



#This is the function to render the Add Recipe page if logged in
@app.route("/addRecipe/<userViewID>", methods=['GET'])
def showRecipeAddForm(userViewID):

	userLoginID = session["user_id"]
	if userLoginID != int(userViewID):
		flash ("Invalid User ID. Here are your recipes.")
		userViewID = userLoginID
		recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
		return render_template("user_recipes.html", display_recipes = recipes)
	else:
		display_recipes = showUserRecipeList(userViewID)
		chems = model.session.query(model.Chem).all()
		chemNames = [chem.chem_name for chem in chems]

	return render_template("add_recipe.html", chem_names = chemNames, user_id = userViewID, display_recipes= display_recipes)





#This function gets the recipe name from the form and adds it to the Recipes table
@app.route("/addRecipe/<userViewID>", methods=['POST'])
def addRecipeName(userViewID):

	display_recipes = showUserRecipeList(userViewID)

	newRecipe = model.Recipe()
	newRecipe.user_id = session["user_id"]
	newRecipe.recipe_name = request.form.get('recipename')

	model.session.add(newRecipe)
	model.session.commit()


	newComp1 = model.Component()
	newComp1.chem_name = request.form.get('chem1')
	newComp1.chem_id = model.Chem.getChemIDByName(newComp1.chem_name)
	newComp1.percentage = request.form.get('percentage1')
	newComp1.recipe_id = newRecipe.id
	model.session.add(newComp1)
	model.session.commit()

	newComp2 = model.Component()
	newComp2.chem_name = request.form.get('chem2')
	newComp2.chem_id = model.Chem.getChemIDByName(newComp2.chem_name)
	newComp2.percentage = request.form.get('percentage2')
	newComp2.recipe_id = newRecipe.id
	model.session.add(newComp2)
	model.session.commit()

	newComp3 = model.Component()
	newComp3.chem_name = request.form.get('chem3')
	newComp3.chem_id = model.Chem.getChemIDByName(newComp3.chem_name)
	newComp3.percentage = request.form.get('percentage3')
	newComp3.recipe_id = newRecipe.id
	model.session.add(newComp3)
	model.session.commit()

	newComp4 = model.Component()
	newComp4.chem_name = request.form.get('chem4')
	newComp4.chem_id = model.Chem.getChemIDByName(newComp4.chem_name)
	newComp4.percentage = request.form.get('percentage4')
	newComp4.recipe_id = newRecipe.id
	model.session.add(newComp4)
	model.session.commit()

	newComp5 = model.Component()
	newComp5.chem_name = request.form.get('chem5')
	newComp5.chem_id = model.Chem.getChemIDByName(newComp5.chem_name)
	newComp5.percentage = request.form.get('percentage5')
	newComp5.recipe_id = newRecipe.id
	model.session.add(newComp5)
	model.session.commit()

	newComp6 = model.Component()
	newComp6.chem_name = request.form.get('chem6')
	newComp6.chem_id = model.Chem.getChemIDByName(newComp6.chem_name)
	newComp6.percentage = request.form.get('percentage6')
	newComp6.recipe_id = newRecipe.id
	model.session.add(newComp6)
	model.session.commit()

	components = model.Component.getComponentsByRecipeID(newRecipe.id)

	newComp = []

	return render_template("recipecomps.html", user_id = userViewID, recipe_name = newRecipe.recipe_name, components = components, newComp = newComp, display_recipes = display_recipes)


# #this is my tester function to add a new component
# @app.route("/addRecipe/<userViewID>/<new_Comp>", methods=['POST'])
# def addRecipeComponent():
# 	newComp = model.Component()
# 	newComp.chem_name = request.form.get('chem')
# 	newComp.chem_id = model.Chem.getChemIDByName(newComp.chem_name)
# 	newComp.percentage = request.form.get('percentage')
# 	# newComp.recipe_id = newRecipe_id
# 	model.session.add(newComp)

# 	return render_template("add_recipe.html", user_id = userViewID)



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
		newComp.append[components.percentage]
		return render_template("recipecomps.html", user_id = userViewID, recipe_name = recipeName, components = components, newComp = newComp, display_recipes=display_recipes)



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
	newComp = []

	for comp in components:
		# print "This is comp percentage", comp.percentage
		newComp.append(comp.percentage)

	for i in range(len(newComp)):
		newComp[i] = float(size) * newComp[i]
	# 	print "This is newComp.percentage", newComp[i]
	# for comp in components:
	# 	print "This is comp percentage", comp.percentage

	return render_template("recipecomps.html", user_id = userViewID, recipe_name = recipeName, newComp = newComp, components = components, display_recipes=display_recipes)






#This function returns the user to the homepage
@app.route("/returnHome")
def returnHome():
	return render_template("index.html")

#This sends you to a way to send a quote to Clay Planet
@app.route("/sendEmailToCP")
def emailCP():
	return render_template("emailCP.html")











def main():
	pass



if __name__ == "__main__":
	app.run(debug=True)

