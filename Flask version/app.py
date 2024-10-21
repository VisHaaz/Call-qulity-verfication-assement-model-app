from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
import csv  # For saving results as CSV
from model import check_call_quality  # Import the function from model.py
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Configure the folder to save uploaded files
app.config['uploaded_audios'] = r'F:\machine learning\qulity model\test model\Flask app\uploaded audios'
app.config['result_csv'] = r'F:\machine learning\qulity model\test model\Flask app\results\call_quality_results.csv'

ALLOWED_EXTENSIONS = {'wav', 'mp3'}  # File extensions allowed for audio files

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading the audio file and saving the result
@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file is submitted
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']

    # Check if the file is valid
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['uploaded_audios'], filename)
        file.save(file_path)  # Save the file to the uploads folder

        # Call your model to check call quality (using transcription + model prediction)
        result = check_call_quality(file_path)

        # Save result to CSV
        csv_file_path = app.config['result_csv']
        save_to_csv(filename, result, csv_file_path)

        return render_template('result.html', result=result)
    
    return redirect(request.url)

# Function to save result to CSV
def save_to_csv(filename, result, csv_file_path):
    file_exists = os.path.isfile(csv_file_path)
    
    with open(csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Filename', 'Verification Result']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Write header if CSV is new

        # Write result to CSV
        writer.writerow({'Filename': filename, 'Verification Result': result})

if __name__ == "__main__":
    app.run(debug=True)  # Run the app in debug mode


