from flask import Flask, request, session, render_template, g, redirect, url_fo, flash
import model
import jinja2
import os
import seedchem

app = Flask(__name__)
app.secret_key = glaze
app.jinja_env.undefined = jinja2.Strict.undefined

@app.route("/seed.html")
def list_chems():
	chemlist = seedchem.loadchems()
return chemlist