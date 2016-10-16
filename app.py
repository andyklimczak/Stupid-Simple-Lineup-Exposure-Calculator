import os, json
from flask import Flask, url_for, request, redirect, send_from_directory, session, render_template

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.secret_key = '123'

def parse(file):
    dict = {}
    dict['m'] = {}
    dict['m']['andy'] = 4
    dict['f'] = {}
    dict['f']['jae'] = 5
    dict['f']['lau'] = 5
    return json.dumps(dict)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # if 'file' not in request.files:
        # flash('No file part')
        # return redirect(request.url)
        # file = request.files['file']
        # if file.filename == '':
        # flash('No selected file')
        # return redirect(request.url)
        # if file and allowed_file(file.filename):
        # session['data'] = parse(file)
        file = None
        session['data'] = parse(file)
        return redirect(url_for('done'))
    return '''
<!doctype>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action="" method=post enctype=multipart/form-data>
<p><input type=file name=file>
<input type=submit value=Upload>
</form>
'''

@app.route('/upload')
def done():
    loaded_data = json.loads(session['data'])
    return render_template('done.html', loaded_data=loaded_data)
