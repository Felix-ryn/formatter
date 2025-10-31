import sys
import os

# 1. Tambahkan direktori induk (formatter) ke Python path
# Ini memastikan Python dapat menemukan 'matrix' dan 'operations'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from flask import Flask, render_template

# ====================================================================
# PERBAIKAN IMPOR: Sekarang impor ini seharusnya stabil karena path sudah ditambahkan
# ====================================================================
# Kita gunakan impor langsung karena direktori induk ('formatter') sudah ada di sys.path
try:
    from matrix import Matrix
    from operations.linear_regression import linear_regression, predict
except ImportError:
    # Ini akan menangkap jika ada masalah di dalam modul itu sendiri,
    # tetapi tidak lagi karena masalah path. Kita biarkan saja pesan warning-nya.
    print("Warning: Gagal mengimpor modul matrix/operations. Pastikan struktur folder sudah benar.")
    
    # Define dummy functions to prevent NameError later
    def linear_regression(X, Y): raise NotImplementedError("linear_regression module failed to load.")
    def predict(x, a, b): raise NotImplementedError("predict module failed to load.")
    Matrix = None


app = Flask(__name__)

# File data ada di direktori kerja saat ini (CWD: ~/formatter)
DATA_FILE_RAW  =  r"/home/felix_ryan/formatter/matriks_a_copy.csv"
COLUMNS = ['Luas', 'Kamar', 'Usia', 'Harga']
LUAS_COL_INDEX = 0
HARGA_COL_INDEX = 3

def load_and_analyze_data():
    """Memuat data dari matriks_a_copy.csv dan menjalankan Simple Linear Regression (SLR)."""
    # Cek impor kritis sebelum mencoba menghitung
    if 'linear_regression' not in globals() and 'linear_regression' not in locals():
        return None, None, {"error": "Gagal menjalankan Regresi: Modul linear_regression tidak ditemukan (ImportError)." }

    try:
        # Menggunakan pandas untuk memuat data tanpa header
        df = pd.read_csv(DATA_FILE_RAW, header=None) 
        df.columns = COLUMNS # Beri nama kolom secara manual
    except FileNotFoundError:
        import os
        return None, None, {"error": f"File data {DATA_FILE_RAW} tidak ditemukan di {os.getcwd()}."}
    except Exception as e:
         return None, None, {"error": f"Gagal membaca data: {e}"}

    # Ambil kolom Luas (index 0) dan Harga (index 3)
    X_luas = df[COLUMNS[LUAS_COL_INDEX]].tolist()
    Y_harga = df[COLUMNS[HARGA_COL_INDEX]].tolist()

    # Hitung Simple Linear Regression (SLR)
    try:
        a, b = linear_regression(X_luas, Y_harga)
    except NotImplementedError as e:
        return None, None, {"error": f"Kesalahan Regresi: {e}. Modul gagal dimuat."}
    except Exception as e:
        return None, None, {"error": f"Kesalahan saat menghitung Regresi: {e}"}
    
    model_slr = {
        'intercept': f"{a:.3f}",
        'slope_luas': f"{b:.3f}",
        'equation': f"Harga = {a:.3f} + {b:.3f} * Luas"
    }
    
    preview_df = df.head(10)
    return df, model_slr, preview_df

@app.route('/')
def index():
    df, model_slr, preview_df = load_and_analyze_data()
    
    if df is None:
        return render_template('index.html', model_slr=None, preview_data=preview_df,chart_data={})

    # Siapkan data untuk Chart.js (hanya Luas dan Harga)
    try:
        chart_data = {
            'luas': df[COLUMNS[LUAS_COL_INDEX]].tolist(),
            'harga': df[COLUMNS[HARGA_COL_INDEX]].tolist(),
            'prediksi': [predict(x, float(model_slr['intercept']), float(model_slr['slope_luas']))[0] 
                        for x in df[COLUMNS[LUAS_COL_INDEX]].tolist()]
        }
    except Exception:
        # Jika predict gagal (karena modul tidak dimuat), kirim data mentah saja
        chart_data = {
            'luas': df[COLUMNS[LUAS_COL_INDEX]].tolist(),
            'harga': df[COLUMNS[HARGA_COL_INDEX]].tolist(),
            'prediksi': []
        }

    # Siapkan data preview sebagai list of lists untuk template
    preview_data = {
        'headers': preview_df.columns.tolist(),
        'rows': preview_df.values.tolist()
    }

    return render_template(
        'index.html',
        model_slr=model_slr,
        preview_data=preview_data,
        chart_data=chart_data
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
