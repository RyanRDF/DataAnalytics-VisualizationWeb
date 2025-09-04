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
        
        # Get processed data table
        table_html, has_data = data_handler.get_raw_data_table()
        
        # Get processing summary
        processing_summary = data_handler.get_processing_summary()
        
        # Clean up the uploaded file
        data_handler.cleanup_file(filepath)
        
        return render_template('index.html', table_html=table_html, has_data=has_data, processing_summary=processing_summary)
        
    except Exception as e:
        return render_template('index.html', table_html="", has_data=False, error=f"Error processing file: {str(e)}")

@app.route('/processing-info')
def processing_info():
    """Get data processing summary"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    processing_summary = data_handler.get_processing_summary()
    return jsonify(processing_summary)

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

@app.route('/keuangan/specific-filter')
def keuangan_specific_filter():
    """Get filtered financial data by specific column value"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not filter_column or not filter_value:
        return jsonify({"error": "Filter column and value are required"}), 400
    
    # Get filtered financial table
    table_html, error = data_handler.get_financial_table_with_specific_filter(
        filter_column, filter_value, sort_column, sort_order, start_date, end_date
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/pasien')
def pasien():
    if not data_handler.has_data():
        return render_template('index.html', table_html="", has_data=False, error="No data available. Please upload a file first.")
    
    # Get patient table
    table_html, error = data_handler.get_patient_table()
    
    if error:
        return render_template('index.html', table_html="", has_data=False, error=error)
    
    return render_template('index.html', table_html=table_html, has_data=True, current_view='pasien')

@app.route('/pasien/sort')
def pasien_sort():
    """Get sorted patient data"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    sort_column = request.args.get('column')
    sort_order = request.args.get('order', 'ASC')
    
    if not sort_column:
        return jsonify({"error": "Column parameter is required"}), 400
    
    # Get sorted patient table
    table_html, error = data_handler.get_patient_table_with_filters(sort_column, sort_order)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/pasien/filter')
def pasien_filter():
    """Get filtered patient data by date range"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    
    # Get filtered patient table
    table_html, error = data_handler.get_patient_table_with_filters(sort_column, sort_order, start_date, end_date)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/pasien/specific-filter')
def pasien_specific_filter():
    """Get filtered patient data by specific column value"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not filter_column or not filter_value:
        return jsonify({"error": "Filter column and value are required"}), 400
    
    # Get filtered patient table
    table_html, error = data_handler.get_patient_table_with_specific_filter(
        filter_column, filter_value, sort_column, sort_order, start_date, end_date
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/pasien/columns')
def pasien_columns():
    """Get available columns for patient data sorting and filtering"""
    columns = data_handler.get_patient_columns()
    return jsonify({"columns": columns})

@app.route('/selisih-tarif')
def selisih_tarif():
    if not data_handler.has_data():
        return render_template('index.html', table_html="", has_data=False, error="No data available. Please upload a file first.")
    
    # Get selisih tarif table
    table_html, error = data_handler.get_selisih_tarif_table()
    
    if error:
        return render_template('index.html', table_html="", has_data=False, error=error)
    
    return render_template('index.html', table_html=table_html, has_data=True, current_view='selisih-tarif')

@app.route('/selisih-tarif/sort')
def selisih_tarif_sort():
    """Get sorted selisih tarif data"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    sort_column = request.args.get('column')
    sort_order = request.args.get('order', 'ASC')
    
    if not sort_column:
        return jsonify({"error": "Column parameter is required"}), 400
    
    # Get sorted selisih tarif table
    table_html, error = data_handler.get_selisih_tarif_table(sort_column, sort_order)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/selisih-tarif/filter')
def selisih_tarif_filter():
    """Get filtered selisih tarif data by date range"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    
    # Get filtered selisih tarif table
    table_html, error = data_handler.get_selisih_tarif_table(sort_column, sort_order, start_date, end_date)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/selisih-tarif/columns')
def selisih_tarif_columns():
    """Get available columns for selisih tarif data"""
    columns = data_handler.get_selisih_tarif_columns()
    return jsonify({"columns": columns})

@app.route('/selisih-tarif/specific-filter')
def selisih_tarif_specific_filter():
    """Get filtered selisih tarif data by specific column value"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not filter_column or not filter_value:
        return jsonify({"error": "Filter column and value are required"}), 400
    
    # Get filtered selisih tarif table
    table_html, error = data_handler.get_selisih_tarif_table_with_specific_filter(
        filter_column, filter_value, sort_column, sort_order, start_date, end_date
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/los')
def los():
    if not data_handler.has_data():
        return render_template('index.html', table_html="", has_data=False, error="No data available. Please upload a file first.")
    
    # Get LOS table
    table_html, error = data_handler.get_los_table()
    
    if error:
        return render_template('index.html', table_html="", has_data=False, error=error)
    
    return render_template('index.html', table_html=table_html, has_data=True, current_view='los')

@app.route('/los/sort')
def los_sort():
    """Get sorted LOS data"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    sort_column = request.args.get('column')
    sort_order = request.args.get('order', 'ASC')
    
    if not sort_column:
        return jsonify({"error": "Column parameter is required"}), 400
    
    # Get sorted LOS table
    table_html, error = data_handler.get_los_table(sort_column, sort_order)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/los/filter')
def los_filter():
    """Get filtered LOS data by date range"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    
    # Get filtered LOS table
    table_html, error = data_handler.get_los_table(sort_column, sort_order, start_date, end_date)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/los/columns')
def los_columns():
    """Get available columns for LOS data"""
    columns = data_handler.get_los_columns()
    return jsonify({"columns": columns})

@app.route('/los/specific-filter')
def los_specific_filter():
    """Get filtered LOS data by specific column value"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not filter_column or not filter_value:
        return jsonify({"error": "Filter column and value are required"}), 400
    
    # Get filtered LOS table
    table_html, error = data_handler.get_los_table_with_specific_filter(
        filter_column, filter_value, sort_column, sort_order, start_date, end_date
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

# INACBG routes
@app.route('/inacbg')
def inacbg():
    """Get INACBG data"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    # Get INACBG table
    table_html, error = data_handler.get_inacbg_table()
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/inacbg/sort')
def inacbg_sort():
    """Get sorted INACBG data"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    sort_column = request.args.get('column')
    sort_order = request.args.get('order', 'ASC')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not sort_column:
        return jsonify({"error": "Column parameter is required"}), 400
    
    # Get sorted INACBG table
    table_html, error = data_handler.get_inacbg_table(sort_column, sort_order, start_date, end_date)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/inacbg/filter')
def inacbg_filter():
    """Get filtered INACBG data by date range"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    
    # Get filtered INACBG table
    table_html, error = data_handler.get_inacbg_table(sort_column, sort_order, start_date, end_date)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/inacbg/columns')
def inacbg_columns():
    """Get available columns for INACBG data"""
    columns = data_handler.get_inacbg_columns()
    return jsonify({"columns": columns})

@app.route('/inacbg/specific-filter')
def inacbg_specific_filter():
    """Get filtered INACBG data by specific column value"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not filter_column or not filter_value:
        return jsonify({"error": "Filter column and value are required"}), 400
    
    # Get filtered INACBG table
    table_html, error = data_handler.get_inacbg_table_with_specific_filter(
        filter_column, filter_value, sort_column, sort_order, start_date, end_date
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

# Ventilator routes
@app.route('/ventilator')
def ventilator():
    if not data_handler.has_data():
        return render_template('index.html', table_html="", has_data=False, error="No data available. Please upload a file first.")
    
    # Get ventilator table
    table_html, error = data_handler.get_ventilator_table()
    
    if error:
        return render_template('index.html', table_html="", has_data=False, error=error)
    
    return render_template('index.html', table_html=table_html, has_data=True, current_view='ventilator')

@app.route('/ventilator/sort')
def ventilator_sort():
    """Get sorted ventilator data"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    sort_column = request.args.get('column')
    sort_order = request.args.get('order', 'ASC')
    
    if not sort_column:
        return jsonify({"error": "Column parameter is required"}), 400
    
    # Get sorted ventilator table
    table_html, error = data_handler.get_ventilator_table(sort_column, sort_order)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/ventilator/filter')
def ventilator_filter():
    """Get filtered ventilator data by date range"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    
    # Get filtered ventilator table
    table_html, error = data_handler.get_ventilator_table(sort_column, sort_order, start_date, end_date)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

@app.route('/ventilator/columns')
def ventilator_columns():
    """Get available columns for ventilator data"""
    columns = data_handler.get_ventilator_columns()
    return jsonify({"columns": columns})

@app.route('/ventilator/specific-filter')
def ventilator_specific_filter():
    """Get filtered ventilator data by specific column value"""
    if not data_handler.has_data():
        return jsonify({"error": "No data available"}), 400
    
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order', 'ASC')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not filter_column or not filter_value:
        return jsonify({"error": "Filter column and value are required"}), 400
    
    # Get filtered ventilator table
    table_html, error = data_handler.get_ventilator_table_with_specific_filter(
        filter_column, filter_value, sort_column, sort_order, start_date, end_date
    )
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"table_html": table_html})

if __name__ == '__main__':
    app.run(debug=True)
