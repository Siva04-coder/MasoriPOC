from flask import Flask, render_template, request, session
import flask
from flask.templating import render_template_string
import json

app = Flask(__name__)
app.secret_key = 'POC1'
login_users = []


@app.route('/home')
def home():
    try:
        if session["username"] == "":
            return render_template('login.html')
    except:
        return render_template('login.html')
    return render_template('land.html')


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/patientsprogression')
def patientsprogression():
    try:
        if session["username"] == "":
            return render_template('login.html')
    except:
        return render_template('login.html')

    session["page_name"] = "Patients Progression"

    return render_template('patients-progression.html')


@app.route('/geolocation')
def geolocation():
    try:
        if session["username"] == "":
            return render_template('login.html')
    except:
        return render_template('login.html')

    session["page_name"] = "Geo Location Mapping"

    return render_template('geo-location-mapping.html')


@app.route('/drugsummary')
def drugsummary():
    try:
        if session["username"] == "":
            return render_template('login.html')
    except:
        return render_template('login.html')

    session["page_name"] = "Drug Summary Statistics"

    return render_template('drug-summary-statistics.html')


@app.route('/brainscan')
def brainscan():
    try:
        if session["username"] == "":
            return render_template('login.html')
    except:
        return render_template('login.html')

    session["page_name"] = "Brain Scan Image Analysis"

    return render_template('brain-scan-image-analysis.html')


@app.route('/patient_details_grid')
def patient_details_grid():

    entPats = db_proxy.get_patient_details('46260', '', '', '')

    return render_template('patient_details_grid.html', results=entPats)


@app.route('/logon', methods=['GET', 'POST'])
def logon():
    print(request.method)
    res = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        res = True

        if res == True:
            login_users.append(username)
            session["username"] = username

    print('sdfasdfads', res)
    return json.dumps(res)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    status = ""

    try:
        session["username"] = ''
        status = "updated"
    except:
        pass

    return status



