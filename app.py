from flask import Flask, render_template, request, send_from_directory, jsonify
import os
from pathlib import Path

# Initialize Flask application
app = Flask(__name__)

# Set up file handling directories
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Route to render index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'message': 'No files part'})
    
    files = request.files.getlist('files[]')
    file_names = []

    for file in files:
        if file and file.filename:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            file_names.append(file.filename)
    
    return jsonify({'uploaded_files': file_names})


# Route to process files (example conversion)
@app.route('/process', methods=['POST'])
def process_files():
    uploaded_files = request.json.get('uploaded_files', [])
    if not uploaded_files:
        return jsonify({'message': 'No files uploaded to process'})

    file_names_argument = ' '.join([f'"{os.path.join(UPLOAD_FOLDER, file)}"' for file in uploaded_files])

    # Assume `tahweel` tool logic is replaced by custom Python processing
    try:
        # Here, you'd call the external processing tool
        # For example: subprocess.run([...])
        
        # Temporary conversion action, e.g., renaming files
        for file_name in uploaded_files:
            base_name = Path(file_name).stem
            pdf_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.pdf")
            docx_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.docx")
            os.rename(os.path.join(UPLOAD_FOLDER, file_name), pdf_path)
            os.rename(pdf_path, docx_path)

        return jsonify({'message': 'Processing completed successfully', 'output_files': uploaded_files})
    
    except Exception as e:
        return jsonify({'message': f"Error during processing: {str(e)}"})


# Route to download files
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
