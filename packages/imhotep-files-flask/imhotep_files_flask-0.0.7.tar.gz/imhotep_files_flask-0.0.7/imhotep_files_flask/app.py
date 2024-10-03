from flask import Flask, request, jsonify
from imhotep_files_flask.main import upload_file, delete_file

app = Flask(__name__)

# Set your upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'.txt', '.jpg'}

@app.route('/upload', methods=['POST'])
def upload():
    file_name = request.form.get('file_name', 'uploaded_file')  # Default name if not provided
    file_path, error = upload_file(request, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, file_name)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'file_path': file_path}), 200

@app.route('/delete', methods=['DELETE'])
def delete():
    file_path = request.json.get('file_path')
    result, error = delete_file(file_path)
    if error:
        return jsonify({'error': error}), 400
    return jsonify({'message': result}), 200

if __name__ == '__main__':
    app.run(debug=True)
