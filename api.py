from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import zipfile
import logging
#import extract_data
from werkzeug.utils import secure_filename


logging.basicConfig(level=logging.DEBUG)

api = Flask(__name__)
# CORS(api)  # Enable CORS
api.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # Set limit to 1 GB

# Directory to store uploaded files
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@api.route('/', methods=['GET', 'POST', 'DELETE'])
def api_files():
    if request.method == 'GET':
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify(files)

    if request.method == 'POST':
        logging.info("Received a POST request")
        if 'file' not in request.files:
            logging.warning("No file part in the request")
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        
        if file.filename == '':
            logging.warning("No selected file")
            return jsonify({'error': 'No selected file'}), 400
        
        print("uploads folder path : ", UPLOAD_FOLDER)
        
        filename = secure_filename(file.filename)
        
        # Save the file to the upload folder
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        logging.info(f"Saving file to {file_path}")
        file.save(file_path)
        print("file_path before : ", file_path)
        file_path = os.path.abspath(file_path)

        print("file_path : ", file_path)


        # extract_response = extract_data.process_file(file_path, filename)   #extract_zip(file_path, EXTRACT_FOLDER,file.filename)

        
        # if "error" in extract_response:
        #     return jsonify({'error': extract_response["error"]}), 500

        # Use jsonify with the response and the appropriate status code
        return jsonify({
            'message': 'File uploaded and extracted successfully',
            'file_path': file_path,
            
        }), 200 #status_code

    if request.method == 'DELETE':
        filename = request.args.get('filename')
        if not filename:
            return jsonify({'error': 'Filename is required for DELETE'}), 400

        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'message': f'File "{filename}" deleted successfully'}), 200
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    api.run(debug=True,use_reloader=False) #host='0.0.0.0', port=8080, 