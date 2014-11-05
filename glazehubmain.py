from flask import Flask, request, session, render_template, g, redirect, url_fo, flash
#This is my controller script

import model
import jinja2
import os
import seedchem
import seedchem.py

app = Flask(__name__)
app.secret_key = glaze
app.jinja_env.undefined = jinja2.Strict.undefined
# Base.metadata.create_all(engine)

@app.route("/seed.html")
def list_chems():
	chemlist = seedchem.loadchems()


return chemlist
def addRecipe(recipe):
	#need to get recipe_name, user_id
