from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/')
def login():
    return render_template('login.html')

    
@app.route('/patients-progression')
def patientsprogression():

    return render_template('patients-progression.html')


@app.route('/logon', methods=['GET', 'POST'])
def logon():
    print(request.method)
    res = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'siva':
            res = 'success'

    print('sdfasdfads', res)
    return res


