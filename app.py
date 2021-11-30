from flask import Flask, render_template, request, session
import flask
from flask.templating import render_template_string
import db_proxy
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

    session["page_name"] = ""

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

    session["page_name"] = "Patient Progression"

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
    entPats = ''

    if request.method == 'POST':
        zipcode = request.form['zipcode']
        city = request.form['city']
        diagnosis = request.form['diagnosis']
        drug = request.form['drug']

        city = city.replace("'", "''")
        diagnosis = diagnosis.replace("'", "''")
        drug = drug.replace("'", "''")

        entPats = db_proxy.get_patient_details(zipcode, city, diagnosis, drug)
        # print(entPats.to_json(orient="index"))

    return entPats.to_json(orient="index")


@app.route('/get_similar_patient_details', methods=['GET', 'POST'])
def get_similar_patient_details():
    entPats = ''

    if request.method == 'POST':
        patientnumber = request.form['patientnumber']
        lifestyle = request.form['lifestyle']

        lifestyle = lifestyle.replace("'", "''''")

        entPats = db_proxy.get_similar_patient_details(
            patientnumber, lifestyle)

        # print(entPats.to_json(orient="index"))

    return entPats.to_json(orient="index")


@app.route('/get_hcp_details', methods=['GET', 'POST'])
def get_hcp_details():
    entPats = ''

    if request.method == 'POST':
        city = request.form['currentCity']

        entPats = db_proxy.get_hcp_details(city)

        # print(entPats.to_json(orient="index"))

    return entPats.to_json(orient="index")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    status = ""

    try:
        session["username"] = ''
        status = "updated"
    except:
        pass

    return status



# if __name__ == "__main__":
#     app.run(debug=True, port=5688)
