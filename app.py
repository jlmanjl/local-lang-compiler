import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from langfunct import *

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'docx', 'doc', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = b'thisissecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    files = []
    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith(".doc") or file.endswith(".docx"):
            os.remove('uploads/' + file)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist("file")
        print(files)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('upload.html', files=files)

@app.route('/compiled')
def langcompiled():
    filelist = path_dict_generator(UPLOAD_FOLDER)
    copylangdict = copy_lang_dict_generator(filelist)
    updatedlangdict = updating_language_dict(copylangdict)
    message_list = print_output(updatedlangdict)

    return render_template('content.html', message_list=message_list)

if __name__ == '__main__':
    app.run(debug = True)