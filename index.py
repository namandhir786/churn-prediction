from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set up directory paths
UPLOAD_FOLDER = 'static/uploads/'
IMAGES_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER
ALLOWED_EXTENSIONS = {'csv'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for index page and file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Load CSV with Pandas
        df = pd.read_csv(filepath)
        # Generate visualizations
        create_visualizations(df)

        return render_template('index.html', message="File uploaded successfully!", images=os.listdir(IMAGES_FOLDER))
    
    return render_template('index.html', message="Invalid file type. Please upload a CSV file.")

# Function to create visualizations from the CSV
def create_visualizations(df):
    # Example: Create a histogram of 'Age' (replace with your column names)
    if 'Age' in df.columns:
        plt.figure(figsize=(8,6))
        df['Age'].hist(bins=30, color='blue', alpha=0.7)
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        # Save the figure
        plt.savefig(os.path.join(IMAGES_FOLDER, 'age_distribution.png'))
        plt.close()

    # Add more visualizations here as per your CSV columns

# Route to display the image files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'], filename)

if __name__ == '__main__':
    app.run(port='5100',debug=True)
