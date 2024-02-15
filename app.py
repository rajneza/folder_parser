from flask import Flask, request, jsonify
from resumeparse import resumeparse
from flask_cors import CORS
import io
from flask_socketio import SocketIO, emit
import os
import re
import docx2txt
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_cors import CORS
import requests
import json


#from io import BytesIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  
class ResumeParser:
    @staticmethod
    def parse_resume(resume_file_path, count, count2,count3, count4, email):
        parser_obj = resumeparse()
        parsed_resume_data = parser_obj.read_file(resume_file_path, count, count2, count3, count4, email)
        print(parsed_resume_data, "99")
        return parsed_resume_data

@app.route('/resumeparse', methods=['POST'])
def parse_resume():

    
    is_folder_upload = request.form.get('isFolderUpload', False)
    count = 0
    count2 = 0
    count3 = 0
    count4 = 0
    batch_count = 0 
    email = []
    if is_folder_upload:
        uploaded_files = request.files.getlist('resumes[]')
        parsed_resume_data_list = []

        for i, resume_file in enumerate(uploaded_files, start=1):
            resume_file_path = new_filename(secure_filename(resume_file.filename), resume_file)
            resume_file.save(resume_file_path)

            parsed_resume_data = ResumeParser.parse_resume(resume_file_path, count, count2,count3, count4, email)
            count = parsed_resume_data['row_newfile']
            count2 = parsed_resume_data['row_oldfile']
            count3 = parsed_resume_data['row_dublicate']
            count4 = parsed_resume_data['none_email']

            os.remove(resume_file_path)
            parsed_resume_data_list.append(parsed_resume_data)
            if i % 10 == 0:
                progress_data = {
                    'current_count': i,
                    'total_count': len(uploaded_files),
                    'new_count': count,
                    'old_count': count2,
                    'dublicate_count': count3,
                    'none_email': count4
                }
                socketio.emit('progress_update', progress_data)

        php_script_url = "http://localhost/folder_parser/username.php"  # Update the URL accordingly
        data = {
        'email': 'example@example.com',
        'domain': '@example.com',
        'row_newfile': count,
        'row_oldfile': count2,
        'row_duplicate': count3,
        'none_email': count4
        }

        response = requests.post(php_script_url, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
        else:
            print("Error communicating with PHP script. Status code:", response.status_code)

        if batch_count * 10 < len(uploaded_files):
            progress_data = {
                'current_count': len(uploaded_files),
                'total_count': len(uploaded_files),
                'new_count': count,
                'old_count': count2,
                'dublicate_count': count3,
                'none_email': count4
            }
            socketio.emit('progress_update', progress_data)

        socketio.emit('parse_complete', {
            'new_count': count,
            'old_count': count2,
        })
              

    return jsonify({
        'new_count': count,
        'old_count': count2,
    })

def new_filename(org_filename, file):
    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S%f")
    unique_filename = f"{timestamp}_{org_filename}"
    return secure_filename(unique_filename)
@app.route('/greet', methods=['POST'])
def greet_user():
    print("hii")
    return jsonify({'message':'hello'})


if __name__ == '__main__':
    app.run(debug=True)