#This is my controller script

import model
import converter
import pricecompute
from flask import Flask, session, render_template, request
from flask import redirect, flash
import jinja2
import json
import smtplib
import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)


app.secret_key = os.environ.get("SECRETKEY")
app.jinja_env.undefined = jinja2.StrictUndefined

# This is the index page. Later it will show the Calculator itself


@app.route("/")
def index():
    session["user_id"] = None
    return render_template("index.html")


@app.route("/logout", methods=['GET'])
def Logout():

    session.clear()

    return redirect("/")


# This is the log in page.
@app.route("/login", methods=['GET'])
def showLoginPage():
    session["user_id"] = None
    return render_template("login.html")


def do_login(userID, userEmail, userName):
    session["user"] = userEmail
    session["user_id"] = userID
    session["user_name"] = userName
    return


# This processes a returning user
@app.route("/process-login", methods=['POST'])
def processLogin():
    session["user_id"] = None
    session["user_name"] = None

    email = request.form.get("userEmail").lower()
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


# This creates a New user
@app.route("/register", methods=['POST'])
def getNewUser():
    session["user_id"] = None
    session["user_name"] = None

    newUser = model.User()
    newUser.user_name = request.form.get("NewUserName")
    newUser.email = request.form.get("NewUserEmail").lower()
    newUser.password = request.form.get("NewUserPassword")
    if model.User.getUserByEmail(newUser.email):
        flash("Email address already exists. Please log on or enter new email")
        return render_template("login.html")
    else:
        model.session.add(newUser)
        model.session.commit()

    flash("Welcome, %s" % (newUser.user_name))
    do_login(newUser.id, newUser.email, newUser.user_name)
    return redirect("/userRecipes/%d" % newUser.id)


#This is the list of recipes of the logged in user
@app.route("/userRecipes/<int:userViewID>")
def listofUserRecipes(userViewID):
    userLoginID = session["user_id"]
    if checkUserLoginID(userLoginID, userViewID) is False:
        flash("Invalid UserID. Here are your recipes")
        userViewID = userLoginID
    recipes = showUserRecipeList(userViewID)
    return render_template("user_recipes.html", displayRecipes=recipes,
                           user_id=userViewID)


# This is the function to render the Enter Recipe page if not logged in
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
    wholeNumList = []
    frctnList = []
    messageToUser = ""
    batchsize = 0.0
    recipename = ""
    percentage = 0.0
    session["chem"] = ""
    session["percentage"] = 0.0

    return render_template("enter_recipe.html", chem_names=chemNames,
                           batchComp=batchComp, user_id=user_id,
                           lbschecked=lbschecked, kgchecked=kgchecked,
                           wholeNumList=wholeNumList,
                           frctnList=frctnList,
                           chem_list=chems, messageToUser=messageToUser,
                           components=components, batchsize=batchsize,
                           recipename=recipename, percentage=percentage)


# This is the function to calculate on the Enter Recipe page if not logged in
@app.route("/enterRecipe", methods=["POST"])
def enterRecipe():

    recipeName = request.form.get('recipename')
    batchsize = request.form.get('batchsize')

    newRecipe = model.Recipe()
    newRecipe.recipe_name = recipeName

    batchComp = []
    sizeflt = float(batchsize)
    kgchecked = 'checked = "checked"'
    lbschecked = ""
    unitSys = "kg"
    percent_list = []
    wholeNumList = []
    frctnList = []
    messageToUser = None

    chem_list = request.values.getlist('chem')
    percentages = request.values.getlist('percentage')
    if percentages == []:
        flash("no entry")
        return redirect("/enterRecipe")

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

    if onehundred is False:
        messageToUser = "Recipe does not add up to 100. Amounts adjusted."
    else:
        messageToUser = None

    for i in range(len(batchComp)):
        batchComp[i] = (sizeflt * batchComp[i])*newPercent

        wholeNumList.append(int(batchComp[i]))
        if unitSys == "kg":
            frctnList.append(int(converter.frctnKilosToGrams(batchComp[i])))
            kgchecked = 'checked = "checked"'
        else:
            frctnList.append(int(converter.frctnPoundsToOunces(batchComp[i])))
            lbschecked = 'checked = "checked"'

    return render_template("calc_recipe.html",
                           recipe_name=newRecipe.recipe_name,
                           chem_list=chem_list, percentages=percentages,
                           batchComp=batchComp, batchsize=batchsize,
                           kgchecked=kgchecked, lbschecked=lbschecked,
                           unitSys=unitSys, wholeNumList=wholeNumList,
                           frctnList=frctnList, messageToUser=messageToUser)


# This is the function to render the Add Recipe page if logged in
@app.route("/addRecipe/<int:userViewID>", methods=['GET'])
def showRecipeAddForm(userViewID):

    recipe_name = ""
    price_quote = float(0.00)
    displayRecipes = showUserRecipeList(userViewID)
    chems = model.session.query(model.Chem).all()
    chemNames = [chem.chem_name for chem in chems]
    components = []

    return render_template("add_recipe.html", chem_names=chemNames,
                           user_id=userViewID,
                           displayRecipes=displayRecipes,
                           recipe_name=recipe_name, components=components,
                           price_quote=price_quote)


# This function gets the recipe name from the form and
# adds it to the Recipes table
@app.route("/addRecipe/<int:userViewID>", methods=["POST"])
def addRecipe(userViewID):

    displayRecipes = showUserRecipeList(userViewID)
    recipe_name = request.form.get('recipename')
    notes = request.form.get('usercomments')

    dupe = model.session.query(model.Recipe)\
        .filter_by(recipe_name=recipe_name)\
        .filter_by(user_id=session["user_id"]).all()

    if dupe != []:
        flash("Duplicate Recipe Name")
        return redirect("/addRecipe/" + str(userViewID))

    newRecipe = model.Recipe()
    newRecipe.user_id = session["user_id"]
    newRecipe.recipe_name = recipe_name
    newRecipe.user_notes = notes

    displayRecipes.append(newRecipe)

    model.session.add(newRecipe)
    model.session.commit()

    batchComp = []
    batchsize = None
    chem_list = request.values.getlist("chem")
    percentages = request.values.getlist("percentage")
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
    wholeNumList = []
    frctnList = []
    messageToUser = None

    components = model.Component.getComponentsByRecipeID(newRecipe.id)

    return render_template("recipecomps.html", user_id=userViewID,
                           recipe_name=newRecipe.recipe_name,
                           components=components, batchComp=batchComp,
                           batchsize=batchsize,
                           displayRecipes=displayRecipes,
                           user_notes=newRecipe.user_notes,
                           kgchecked=kgchecked, lbschecked=lbschecked,
                           unitSys=unitSys, wholeNumList=wholeNumList,
                           frctnList=frctnList, messageToUser=messageToUser)


#this is the recipe page, checks user too
@app.route("/recipecomps/<int:userViewID>/<recipeName>")
def recipe(userViewID, recipeName):

    displayRecipes = showUserRecipeList(userViewID)

    userLoginID = session["user_id"]

    if checkUserLoginID(userLoginID, userViewID) is False:
        userViewID = userLoginID
        recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
        return render_template("user_recipes.html", displayRecipes=recipes,
                               user_id=userLoginID)
    else:
        recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
        components = model.Component.getComponentsByRecipeID(recipe.id)

    messageToUser = None

    price_quote = 0.00
    batchComp = []
    wholeNumList = []
    frctnList = []
    batchsize = None

    unit_sys = "unitSys"
    lbschecked = ""
    kgchecked = 'checked = "checked"'

    return render_template("/recipecomps.html/", user_id=userViewID,
                           recipe_name=recipeName, components=components,
                           batchComp=batchComp,
                           displayRecipes=displayRecipes,
                           user_notes=recipe.user_notes,
                           messageToUser=messageToUser,
                           unitSys=unit_sys, batchsize=batchsize,
                           wholeNumList=wholeNumList, frctnList=frctnList,
                           lbschecked=lbschecked, kgchecked=kgchecked,
                           price_quote=price_quote)


# This section allows the user to change batchsizes
@app.route("/recipecomps/<userViewID>/<recipeName>",  methods=["POST"])
def batchSizeChange(userViewID, recipeName):
    displayRecipes = showUserRecipeList(userViewID)
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

    if onehundred is False:
        messageToUser = "Recipe does not add up to 100. Amount adjusted."
    else:
        messageToUser = None

    x = 0
    for comp in components:
        batchComp.append(comp.percentage/100)
        x += 1

    sizeflt = float(size)
    wholeNumList = []
    frctnList = []
    kgchecked = ""
    lbschecked = ""
    priceList = []
    compList = []

    j = 0
    for i in range(len(batchComp)):

        batchComp[i] = (sizeflt * batchComp[i])*newPercent
        chemID = model.Chem.getChemIDByName(components[j].chem.chem_name)

        wholeNumList.append(int(batchComp[i]))

        if units == "kg":
            frctnList.append(int(converter.frctnKilosToGrams(batchComp[i])))
            kgchecked = 'checked = "checked"'
            kgToPounds = converter.poundsToKilos(batchComp[i])
            chemPrice = pricecompute.getPrice(chemID, kgToPounds)
            priceList.append(chemPrice * batchComp[i])
        else:
            frctnList.append(int(converter.frctnPoundsToOunces(batchComp[i])))
            lbschecked = 'checked = "checked"'
            chemPrice = pricecompute.getPrice(chemID, batchComp[i])
            priceList.append(chemPrice * batchComp[i])

        dict_of_comp = {
            'a_name': components[j].chem.chem_name[:35],
            'b_percent': components[j].percentage,
            'c_whole': wholeNumList[i],
            'd_frctn': frctnList[i],
            'e_chemPrice': priceList[i]
        }

        compList.append(dict_of_comp)
        j += 1

    sumprice = sum(priceList)

    if units == "kg":
        surcharge = pricecompute.getSurChargeKilos(sizeflt) * len(batchComp)
        session["surcharge"] = surcharge
        shipping = pricecompute.getShipping(converter.poundsToKilos(sizeflt))
    else:
        surcharge = pricecompute.getSurChargeLbs(sizeflt) * len(batchComp)
        session["surcharge"] = surcharge
        shipping = pricecompute.getShipping(sizeflt)

    session["shipping"] = shipping
    session["pre-tax-cost"] = round(sumprice, 2)

    if sizeflt == 0:
        price_quote = 0
    else:
        price_quote = round((sumprice + surcharge), 2)

    orderItems = json.dumps(compList, sort_keys=True,
                            separators=(',', ': '))
    session["orderList"] = orderItems

    if (lbschecked == 'checked = "checked"'):
        session["unitSys"] = "lbs"
    else:
        session["unitSys"] = "kilos"

    return render_template("recipecomps.html", user_id=userViewID,
                           recipe_name=recipeName, batchComp=batchComp,
                           components=components,
                           displayRecipes=displayRecipes,
                           user_notes=recipe.user_notes,
                           messageToUser=messageToUser, batchsize=size,
                           wholeNumList=wholeNumList, frctnList=frctnList,
                           kgchecked=kgchecked, lbschecked=lbschecked,
                           unitSys=units, price_quote=price_quote,
                           compList=compList, orderItems=orderItems)


@app.route("/editRecipe/<userViewID>/<recipeName>", methods=['GET'])
def showEditRecipeForm(userViewID, recipeName):

    userLoginID = session["user_id"]
    recipe_name = recipeName

    if userLoginID != int(userViewID):
        flash("Invalid User ID. Here are your recipes. 2")
        userViewID = userLoginID
        recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
        return render_template("user_recipes.html", user_id=userViewID,
                               displayRecipes=recipes)
    else:
        displayRecipes = showUserRecipeList(userViewID)
        chems = model.session.query(model.Chem).all()
        chemNames = [chem.chem_name for chem in chems]
        recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
        components = model.Component.getComponentsByRecipeID(recipe.id)
        user_notes = recipe.user_notes

    return render_template("edit_recipe.html", chem_names=chemNames,
                           user_id=userViewID,
                           displayRecipes=displayRecipes,
                           recipe_name=recipe_name, components=components,
                           user_notes=user_notes)


@app.route("/editRecipe/<int:userViewID>/<recipeName>", methods=["POST"])
def updateRecipe(userViewID, recipeName):
    user_id = userViewID
    recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
    recipe.recipe_name = request.form.get("recipe_name")
    recipe.user_notes = request.form.get("user_notes")
    recipeName = recipe.recipe_name

    components = model.Component.getComponentsByRecipeID(recipe.id)

    # Get rid of old recipe components
    for comp in components:
        model.session.delete(comp)
        model.session.commit()

    # Get new values for recipe components, names and percentages
    chem_list = request.form.getlist("chem")
    percentages = request.form.getlist("percentage")

    i = 0
    for chem in chem_list:
        addComp = model.Component()
        addComp.chem_name = chem
        addComp.chem_id = model.Chem.getChemIDByName(addComp.chem_name)
        addComp.percentage = float(percentages[i])
        addComp.recipe_id = recipe.id
        if (percentages[i] != 0) or percentages[i]:
            model.session.add(addComp)
            model.session.commit()
            i += 1
        else:
            model.session.commit()

    return redirect("/recipecomps/%d/%s" % (user_id, recipeName))


@app.route("/deleteRecipe/<int:userViewID>/<recipeName>", methods=['GET'])
def deleteRecipe(userViewID, recipeName):
    user_id = userViewID

    recipe = model.Recipe.getRecipeIDByName(recipeName, userViewID)
    components = model.Component.getComponentsByRecipeID(recipe.id)
    model.session.delete(recipe)

    for comp in components:
        model.session.delete(comp)
    model.session.commit()

    return redirect("/userRecipes/%d" % user_id)


#This sends you to a way to send a quote to Clay Planet
@app.route("/emailCP/<int:userViewID>/<recipeName>/<batchSize>",
           methods=['GET'])
def emailCP(userViewID, recipeName, batchSize):
    displayRecipes = showUserRecipeList(userViewID)
    user_id = userViewID
    recipeName = recipeName
    unitSys = session["unitSys"]
    subtotal = session["pre-tax-cost"] + session["surcharge"]
    shipping_cost = session["shipping"]
    msgSent = False
    session["batchSize"] = batchSize

    tax = pricecompute.getTax(subtotal)

    session["tax"] = tax

    orderList = session["orderList"]
    data = json.loads(orderList)

    return render_template("emailCP.html", user_id=user_id,
                           displayRecipes=displayRecipes,
                           recipeName=recipeName, batchsize=batchSize,
                           data=data, unitSys=unitSys, subtotal=subtotal,
                           shipping=shipping_cost, tax=tax, msgSent=msgSent)


@app.route("/emailCP/<int:userViewID>/<recipeName>/<batchSize>",
           methods=["POST"])
def emailCPSend(userViewID, recipeName, batchSize):
    displayRecipes = showUserRecipeList(userViewID)
    user_name = session["user_name"]
    user_id = userViewID
    unitSys = session["unitSys"]
    batchSize = session["batchSize"]
    if unitSys == "lbs":
        wholesys = "lbs"
        frctnsys = "oz"
    else:
        wholesys = "kgs"
        frctnsys = "grms"

    customer = session["user"]

    msgToCP = request.form.get("msgToCP")

    orderList = session["orderList"]

    data = json.loads(orderList)

    surcharge = round(session["surcharge"], 2)
    tax = round(session["tax"], 2)
    subtotal = round(session["pre-tax-cost"], 2)
    shipping = round(session["shipping"], 2)

    price_quote = tax + subtotal + shipping + surcharge

    order_time = str(datetime.datetime.utcnow())

    gmail_user = "glazehub@gmail.com"
    gmail_pwd = os.environ.get("EMAILPASSWORD")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Glaze Order" + order_time
    msg['From'] = gmail_user
    msg['To'] = "marlenehirose@gmail.com"

    text = "Order from: " + customer + "\n" + \
           "Message from Customer: " + msgToCP + "\n" + \
           "Recipe Name: " + recipeName + "\n" +\
           "Pounds/Kilos: " + wholesys + " " + frctnsys + "\n\n" +\
           "SubTotal: %.2f " % (subtotal+surcharge) + "\n"\
           "Tax: %.2f" % tax + "\n" + \
           "Shipping: %.2f" % shipping + "\n"\
           "Price Quote: %.2f" % price_quote

    html = render_template("email.html", recipeName=recipeName, data=data,
                           batchsize=batchSize, unitSys=unitSys,
                           customer=customer, subtotal=subtotal,
                           surcharge=surcharge, shipping=shipping, tax=tax,
                           msgToCP=msgToCP, user_name=user_name)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    FROM = gmail_user
    TO = ["marlenehirose@gmail.com"]

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, msg.as_string())
    server.close()

    msgSent = True

    return render_template("emailCP.html", user_id=user_id,
                           displayRecipes=displayRecipes,
                           userName=user_name, msgSent=msgSent)


# This function displays all recipes for the particular user
def showUserRecipeList(userViewID):
    userLoginID = session["user_id"]
    if checkUserLoginID(userLoginID, userViewID):
        recipes = model.Recipe.getRecipeNamesByUserID(userLoginID)
        return recipes
    else:
        recipes = model.Recipe.getRecipeNamesByUserID(userViewID)
        return recipes


# This function checks userLogin and userViewID to make sure that
# logged in user only sees their own recipes
def checkUserLoginID(userLoginID, userViewID):
    if userLoginID != int(userViewID):
        flash("Invalid User ID. Here are your recipes")
        userViewID = userLoginID
        return False


def main():
    pass


if __name__ == "__main__":
    app.run(debug=True)
