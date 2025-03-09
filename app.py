import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import uuid

from app.config.config import MAX_CONTENT_LENGTH
from app.utils.file_utils import (
    allowed_file, get_file_extension, UPLOAD_DIR
)
from app.converters.converter import FileConverter

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    output_format = request.form.get('output_format')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save the uploaded file
            original_filename = secure_filename(file.filename)
            temp_filename = f"temp_{str(uuid.uuid4())}.{original_filename.split('.')[-1]}"
            input_path = os.path.join(UPLOAD_DIR, temp_filename)
            file.save(input_path)
            
            # Convert the file
            output_filename = f"converted_{str(uuid.uuid4())}.{output_format}"
            output_path = os.path.join(UPLOAD_DIR, output_filename)
            
            # Convert using the appropriate method
            input_format = get_file_extension(input_path)
            FileConverter.convert_file(input_path, output_path, input_format, output_format)
            
            # Clean up input file
            if os.path.exists(input_path):
                os.remove(input_path)
            
            return jsonify({
                'message': 'File converted successfully',
                'filename': output_filename
            })
        except Exception as e:
            # Clean up any files on error
            if os.path.exists(input_path):
                os.remove(input_path)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Get the original name without the UUID
        extension = filename.split('.')[-1]
        download_name = f"converted_file.{extension}"

        return send_file(
            file_path,
            as_attachment=True,
            download_name=download_name
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True) 