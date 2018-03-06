from flask import Flask, render_template, redirect, url_for, request

import motie_photo_news as motie

app = Flask("Project")

@app.route("/index")
def welcome():
    return render_template("index.html")

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# Route for handling tables
@app.route("/tables")
def show_tables():
    data = motie.motie_photo_news
    data.set_index(['Name'], inplace=True)
    data.index.name=None
    return render_template('view.html',table=[data.to_html],
    titles = ['MOTIE'])

app.run(debug = True)
