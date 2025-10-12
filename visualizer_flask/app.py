import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Tentukan path relatif ke file CSV Anda
CSV_FILE_PATH = '../matriks_a_copy.csv'

def get_chart_data():
    """
    Memuat data CSV dan mengembalikan PYTHON DICT.
    
    PENTING: Tidak ada json.dumps() di sini.
    """
    try:
        df = pd.read_csv(CSV_FILE_PATH, header=None)
        
        labels = df[0].astype(str).tolist()
        values = df[3].tolist()

        chart_data = {
            'labels': labels,
            'data_values': values,
            'dataset_label': 'Nilai Matriks (Kolom 3)'
        }
        
        # Mengembalikan DICT
        return chart_data 

    except FileNotFoundError:
        print(f"ERROR: File CSV tidak ditemukan di {CSV_FILE_PATH}")
        return {'labels': ["Error"], 'data_values': [0], 'dataset_label': 'File Not Found'}
    except Exception as e:
        print(f"ERROR: Kesalahan saat memproses data: {e}")
        return {'labels': ["Error"], 'data_values': [0], 'dataset_label': 'Data Error'}

@app.route('/')
def index():
    data_dict = get_chart_data() 
    # Meneruskan DICT ke template
    return render_template('index.html', chart_data=data_dict) 

if __name__ == '__main__':
    app.run(debug=True)
