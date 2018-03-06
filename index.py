from flask import Flask, render_template, redirect, url_for, request

import motie_photo_news as motie
import pandas as pd

app = Flask("Project")

@app.route("/access")
def access():
    return render_template("trial.html")

@app.route("/test",methods=["POST"])
def date_accessed():
    form_data = request.form
    date = form_data['dateaccessed']
    data = motie.produce_motie_df(date)
    return render_template('view.html',table=[data.to_html()])

app.run(debug = True)
