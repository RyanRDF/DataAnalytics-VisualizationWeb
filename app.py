from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'instance/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Baca data sesuai ekstensi
    if file.filename.endswith('.txt'):
        df = pd.read_csv(filepath, sep=';')
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        return "Format file tidak didukung"

    # Convert dataframe to HTML table and pass it to the template
    table_html = df.to_html(classes='data-table', index=False)
    return render_template('index.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)
