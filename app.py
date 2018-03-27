from flask import Flask, render_template, redirect, url_for, request

import news_compiler as nc
import pandas as pd

app = Flask(__name__)

@app.route("/access")
def access():
    return render_template("welcome.html")

@app.route("/news",methods=["POST"])
def date_accessed():
    form_data = request.form
    date = form_data['dateaccessed']
    data = nc.news_df_producer(date)
    table = data.to_html()
    table = table.strip('[u')
    table = table.strip("']")
    table = table.strip('\n')
    return render_template('view.html',table=table)

if __name__ == '__main__':
    app.run(debug = True)
