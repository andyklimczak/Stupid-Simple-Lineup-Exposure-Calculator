import os, json, csv, io
import pandas as pd
from collections import defaultdict
from flask import Flask, url_for, request, redirect, send_from_directory, session, render_template

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = '123'

def calculate(data):
    print(type(data).__name__)
    dict = defaultdict(int)
    for player in data:
        dict[player] += 1
    return dict

def parse(file):
    dict = {}
    with io.StringIO(file.stream.read().decode("UTF8"), newline=None) as csv_file:
        data = pd.read_csv(csv_file)
        dict['QB'] = calculate(data['QB'])
        dict['FLEX'] = calculate(pd.concat([data['WR'], data['RB']]))
    return json.dumps(dict)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            session['data'] = parse(file)
            return redirect(url_for('done'))
    return render_template("index.html")

@app.route('/upload')
def done():
    loaded_data = json.loads(session['data'])
    return render_template('done.html', loaded_data=loaded_data)
