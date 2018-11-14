import csv
import io
import json
import requests
from flask import Flask, request, flash, redirect
from Settings import ALLOWED_EXTENSIONS


# EB looks for an 'application' callable by default.
application = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'Please upload a csv file'

        up_file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if up_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if up_file and allowed_file(up_file.filename):
            stream = io.StringIO(request.files['file'].read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            json_data = list()
            for row in csv_input:
                if 0 < len(row[0].split(' ')) <= 5 and 8 < len(row[1].split(' ')):
                    data = dict()
                    data['type'] = row[0]
                    data['content'] = row[1]
                    json_data.append(data)
            json_data = json.dumps(json_data)
            requests.post('http://68.183.58.223/predict', json=json_data)
            response = requests.get('http://68.183.58.223')
            print response

            return 'successfully uploaded'
    return '''
        <!doctype html>
        <title>Upload a csv file for document classification</title>
        <h1>Upload csv File only</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.secret_key = 'super secret key'
    application.config['SESSION_TYPE'] = 'filesystem'
    application.run()
