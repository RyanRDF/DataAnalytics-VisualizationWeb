from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'instance/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Don't load sample data by default - table will only show after file upload
    return render_template('index.html', table_html="", has_data=False)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    
    # Check if file is a .txt file
    if not file.filename.endswith('.txt'):
        return render_template('index.html', table_html="", has_data=False, error="Please upload a .txt file")
    
    try:
        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Read the uploaded file with tab separator (same format as sampel_data.txt)
        df = pd.read_csv(filepath, sep='\t')
        
        # Convert dataframe to HTML table
        table_html = df.to_html(classes='data-table', index=False)
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return render_template('index.html', table_html=table_html, has_data=True)
        
    except Exception as e:
        return render_template('index.html', table_html="", has_data=False, error=f"Error processing file: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
