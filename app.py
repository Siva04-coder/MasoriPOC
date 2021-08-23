from flask import Flask, render_template, request, session
import flask
from flask.templating import render_template_string
import db_proxy, json

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

    
@app.route('/patients-progression')
def patientsprogression():
    try:
        if session["username"] == "":
            return render_template('login.html')
    except:
        return render_template('login.html')

    return render_template('patients-progression.html')


@app.route('/patient_details_grid')
def patient_details_grid():

    entPats = db_proxy.get_patient_details('46260','','','')

    return render_template('patient_details_grid.html', results = entPats)


@app.route('/logon', methods=['GET', 'POST'])
def logon():
    print(request.method)
    res = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        res = db_proxy.check_user(username, password)
        
        if res == True:
            login_users.append(username)
            session["username"] = username

    print('sdfasdfads', res)
    return json.dumps(res)

@app.route('/get_city', methods=['GET', 'POST'])
def get_city():
    cities = db_proxy.get_city()
    return json.dumps(cities)

@app.route('/get_diagnosis', methods=['GET', 'POST'])
def get_diagnosis():
    ent = db_proxy.get_diagnosis()
    return json.dumps(ent)

@app.route('/get_drug', methods=['GET', 'POST'])
def get_drug():
    entDrug = db_proxy.get_drug()
    return json.dumps(entDrug)

@app.route('/get_patient_details', methods=['GET', 'POST'])
def get_patient_details():
    entPats = db_proxy.get_patient_details('46260','','','')
    print(entPats.to_json())
    return flask.jsonify({'data': entPats})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    status = ""

    try:
        session["username"] = ''
        status = "updated"
    except:
        pass

    return status

app.run(port=4858)
