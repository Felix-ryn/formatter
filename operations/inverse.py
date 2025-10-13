# inverse.py
from matrix import Matrix
# Pastikan impor relatif yang benar untuk find_determinant (dari file .determinant)
from .determinant import find_determinant 
from validators.is_square import is_square

def inverse_matrix(matrix):
    """
    Menghitung invers matriks 2x2 atau 3x3.
    """
    data = matrix.data
    if not is_square(data):
        raise ValueError("Matrix harus persegi untuk menghitung invers.")

    n = len(data)
    # PENTING: find_determinant membutuhkan objek Matrix. Jika Anda menggunakan list (data)
    # untuk mencari minor 3x3, Anda harus mengubah find_determinant agar menerima list.
    # Karena sintaks Anda menunjukkan find_determinant menerima Matrix, kita buat Matrix baru.
    
    # 1. Hitung Determinan dari objek Matrix
    det = find_determinant(matrix) 
    
    if det == 0:
        raise ValueError("Matriks singular, tidak memiliki invers.")

    # Kasus 2x2
    if n == 2:
        a, b = data[0]
        c, d = data[1]
        inv_data = [[d/det, -b/det], [-c/det, a/det]]
        return Matrix(inv_data)

    # Kasus 3x3 (pakai kofaktor)
    elif n == 3:
        cofactor = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                # Ekstrak minor sebagai list of lists
                minor_list = [
                    [data[x][y] for y in range(3) if y != j]
                    for x in range(3) if x != i
                ]
                sign = (-1) ** (i + j)
                
                # UBAH: Untuk minor (2x2) kita kirim List of List ke find_determinant, 
                # ASUMSI find_determinant dapat memproses list untuk 2x2 (seperti di kode Anda sebelumnya)
                # JIKA find_determinant HANYA menerima Matrix, ini adalah BUG!
                
                # SOLUSI PALING AMAN: Pastikan find_determinant di determinant.py menerima list
                # atau buat objek Matrix dari minor_list:
                minor_det = find_determinant(Matrix(minor_list)) 
                
                cofactor[i][j] = sign * minor_det
                
        # transpose kofaktor
        cofactor_T = [[cofactor[j][i] for j in range(3)] for i in range(3)]
        inv_data = [[cofactor_T[i][j] / det for j in range(3)] for i in range(3)]
        return Matrix(inv_data)

    else:
        # Perlu dikoreksi: find_determinant di atas hanya dipanggil dengan Matrix.
        # Jika find_determinant Anda hanya menerima Matrix, pastikan minor_list diubah ke Matrix.
        raise NotImplementedError("Inverse hanya didukung untuk matriks 2x2 dan 3x3.")
