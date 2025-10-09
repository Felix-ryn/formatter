# json_exporter.py
import json

def export_to_json(matriks, nama_file):
    """
    Fungsi untuk mengekspor data matriks ke file JSON.
    :param matriks: Objek matriks (harus memiliki attribute .data berupa list of lists)
    :param nama_file: Nama file output JSON.
    """
    try:
        matriks_data = matriks.data
        with open(nama_file, 'w') as file:
            json.dump(matriks_data, file, indent=4)
        print(f"✅ Matriks berhasil diekspor ke {nama_file}")
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat mengekspor ke JSON: {e}")
