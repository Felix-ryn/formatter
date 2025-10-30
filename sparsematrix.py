# sparsematrix.py
"""SparseMatrix: menyimpan hanya elemen != 0, tetapi menyediakan .data sebagai list-of-lists on-demand."""

from validators.is_square import is_square
from validators.is_symmetric import is_symmetric

"""
Modul ini berisi kelas SparseMatrix dengan komentar diperluas.
SparseMatrix menyimpan hanya elemen yang bukan nol dalam bentuk kamus (dict)
untuk menghemat memori dan mempercepat operasi tertentu.
Penambahan komentar dilakukan agar setiap bagian kode lebih mudah dipahami.
"""

class SparseMatrix:
    """
    Representasi matriks jarang (sparse).
    """
    def __init__(self, data):
        self._sparse_data = {}
        self._dense_cache = None

        if isinstance(data, dict):
            self._sparse_data = dict(data)
            if self._sparse_data:
                self.rows = max(i for i, _ in self._sparse_data.keys()) + 1
                self.cols = max(j for _, j in self._sparse_data.keys()) + 1
            else:
                self.rows = self.cols = 0
        else:
            if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
                raise TypeError("Data harus berupa list of lists atau dict {(i,j): val}.")
            self.rows = len(data)
            self.cols = len(data[0]) if self.rows > 0 else 0
            if not all(len(row) == self.cols for row in data):
                raise ValueError("Semua baris harus memiliki jumlah kolom yang sama.")
            for r, row in enumerate(data):
                for c, val in enumerate(row):
                    if val != 0:
                        self._sparse_data[(r, c)] = val

    @property
    def data(self):
        if self._dense_cache is not None:
            return self._dense_cache
        dense = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for (r, c), v in self._sparse_data.items():
            dense[r][c] = v
        self._dense_cache = dense
        return self._dense_cache

    def is_square(self):
        return is_square(self.data)

    def is_symmetric(self):
        return is_symmetric(self.data)

    def get_value(self, row, col):
        return self._sparse_data.get((row, col), 0)

    def __repr__(self):
        return f"SparseMatrix(rows={self.rows}, cols={self.cols}, nnz={len(self._sparse_data)})"

    def __str__(self):
        return "\n".join(
            " ".join(str(self.get_value(r, c)) for c in range(self.cols))
            for r in range(self.rows)
        )
