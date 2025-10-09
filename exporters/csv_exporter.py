# csv_exporter.py
import csv

def export_to_csv(matriks, nama_file):
    """
    Fungsi untuk mengekspor data matriks ke file CSV.
    :param matriks: Objek matriks (harus memiliki attribute .data berupa list of lists)
    :param nama_file: Nama file output CSV.
    """
    try:
        with open(nama_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in matriks.data:
                writer.writerow(row)
        print(f"✅ Matriks berhasil diekspor ke {nama_file}")
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat mengekspor ke CSV: {e}")
