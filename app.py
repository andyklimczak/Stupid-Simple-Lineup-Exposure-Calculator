import os, json, csv, io, math
import pandas as pd
from collections import defaultdict, OrderedDict
from flask import Flask, url_for, request, redirect, send_from_directory, session, render_template, flash

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = '123'

def calculateFootball(data, count):
    dict = {};
    dict['QB'] = calculate(data['QB'], count)
    dict['FLEX'] = calculate(pd.concat([data['RB'], data['RB.1'], data['WR'], data['WR.1'], data['WR.2'], data['TE'], data['FLEX']]), count)
    dict['DST'] = calculate(data['DST'], count)
    return dict

def calculateBasketball(data, count):
    dict = {};
    dict['BALLERS'] = calculate(pd.concat([data['PG'], data['SG'], data['SF'], data['PF'], data['C'], data['G'], data['F'], data['UTIL']]), count)
    return dict

def number_of_lineups(col):
    count = 0
    for row in col:
        if not math.isnan(row):
            count += 1
    return count

def regex_player_name(playerName):
    return playerName[:playerName.index('(')]

def calculate(data, count):
    dict = defaultdict(int)
    for player in data:
        if type(player) is not float: # check for nan
            playerName = regex_player_name(player)
            dict[playerName] += 1 / count
    return dict

def parse(file):
    with io.StringIO(file.stream.read().decode("UTF8"), newline=None) as csv_file:
        data = pd.read_csv(csv_file)
        count = number_of_lineups(data['Entry ID'])
        dict = {};
        if 'QB' in data.columns:
            dict = calculateFootball(data, count)
        elif 'PG' in data.columns:
            dict = calculateBasketball(data, count)
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
    return render_template('done.html', data=loaded_data)
