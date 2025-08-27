from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from processing import DataHandler

app = Flask(__name__)

UPLOAD_FOLDER = 'instance/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize data handler
data_handler = DataHandler()

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
    
    # Validate file
    is_valid, error = data_handler.validate_file(file.filename)
    if not is_valid:
        return render_template('index.html', table_html="", has_data=False, error=error)
    
    try:
        # Save the uploaded file
        filepath, error = data_handler.save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
        if error:
            return render_template('index.html', table_html="", has_data=False, error=error)
        
        # Load data from file
        df, error = data_handler.load_data_from_file(filepath)
        if error:
            data_handler.cleanup_file(filepath)
            return render_template('index.html', table_html="", has_data=False, error=error)
        
        # Get raw data table
        table_html, has_data = data_handler.get_raw_data_table()
        
        # Clean up the uploaded file
        data_handler.cleanup_file(filepath)
        
        return render_template('index.html', table_html=table_html, has_data=has_data)
        
    except Exception as e:
        return render_template('index.html', table_html="", has_data=False, error=f"Error processing file: {str(e)}")

@app.route('/keuangan')
def keuangan():
    if not data_handler.has_data():
        return render_template('index.html', table_html="", has_data=False, error="No data available. Please upload a file first.")
    
    # Get financial table
    table_html, error = data_handler.get_financial_table()
    
    if error:
        return render_template('index.html', table_html="", has_data=False, error=error)
    
    return render_template('index.html', table_html=table_html, has_data=True, current_view='keuangan')

@app.route('/keuangan/sort')
def keuangan_sort():
    """Get sorted financial data"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    sort_column = request.args.get('column')
    sort_order = request.args.get('order', 'ASC')
    
    if not sort_column:
        return jsonify({"error": "Column parameter is required"}), 400
    
    # Get sorted financial table
    table_html, error = data_handler.get_financial_table(sort_column, sort_order)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/keuangan/filter')
def keuangan_filter():
    """Get filtered financial data by date range"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    
    # Get filtered financial table
    table_html, error = data_handler.get_financial_table(sort_column, sort_order, start_date, end_date)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/keuangan/columns')
def keuangan_columns():
    """Get available columns for financial data"""
    columns = data_handler.get_financial_columns()
    return jsonify({"columns": columns})

@app.route('/pasien')
def pasien():
    if not data_handler.has_data():
        return render_template('index.html', table_html="", has_data=False, error="No data available. Please upload a file first.")
    
    # Get patient table
    table_html, error = data_handler.get_patient_table()
    
    if error:
        return render_template('index.html', table_html="", has_data=False, error=error)
    
    return render_template('index.html', table_html=table_html, has_data=True, current_view='pasien')

if __name__ == '__main__':
    app.run(debug=True)
