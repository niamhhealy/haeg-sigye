from flask import Flask, render_template

app = Flask("Project")

@app.route("/index")
def welcome():
    return render_template("index.html")

app.run(debug = True)
