import os
from datetime import datetime
from typing import List, Any
from zipfile import ZipFile
import zipfile

from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_DIR'] = os.path.join('static','UPLOADS')

errors: List[str] = []

def isVaildExt(file_name):
    return '.' in file_name and '.sb3' in os.path.splitext(file_name)

@app.route('/')
def hello_world():
    return render_template('index.html',errs = errors)

@app.route('/send',methods=['GET','POST'])
def send():
    if request.method == 'POST':
        uploaded_file: FileStorage = request.files['uploaded_file']
        if uploaded_file and isVaildExt(uploaded_file.filename):
            #save_file_name = datetime.now().strftime('%Y%m%d_%H%M%S')+secure_filename(uploaded_file.filename)
            #uploaded_file.save(os.path.join(app.config['UPLOAD_DIR'],save_file_name))
            with tempfile.TemporaryDirectory() as extract_dir:
               # print(extract_dir)
                with ZipFile(uploaded_file, 'r') as test_zip:
                    test_zip.extractall(extract_dir)
                    JsonData = ''
                    if os.path.exists(extract_dir+r'/project.json'):
                        with open(extract_dir+r'/project.json','r',encoding='utf-8') as json:
                            JsonData = (json.read()).replace(r'\b','')
                        with open(extract_dir+r'/project.json','w',encoding='utf-8') as json:
                            json.write(JsonData)
                        #print(os.listdir(extract_dir))
                        with tempfile.NamedTemporaryFile(delete=False) as out:
                           # print(os.listdir(extract_dir))
                            with ZipFile(out, 'w',compression=zipfile.ZIP_STORED) as exportfile:
                                print(os.listdir(extract_dir))
                                for filename in os.listdir(extract_dir):
                                        print(filename)
                                        exportfile.write(os.path.join(extract_dir,filename), arcname=filename)
                        return send_file(out.name,as_attachment=True,attachment_filename='New_'+uploaded_file.filename)
                    else:
                        return 'Error:Not exits /project.json'
        else:
            errors.append('対応する拡張子は『.sb3』のみです.')
            return redirect(url_for('hello_world'))




if __name__ == '__main__':
    app.run(debug=True)
