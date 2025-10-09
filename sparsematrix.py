# sparsematrix.py
"""SparseMatrix: menyimpan hanya elemen != 0, tetapi menyediakan .data sebagai list-of-lists on-demand."""

class SparseMatrix:
    """
    Representasi matriks jarang (sparse).
    Input dapat berupa:
      - list of lists (dense), atau
      - dict {(row, col): value} (sparse)
    Atribut yang tersedia:
      - rows, cols
      - data  (property, list of lists)
      - get_value(r,c)
    """
    def __init__(self, data):
        # internal sparse storage
        self._sparse_data = {}
        self._dense_cache = None

        if isinstance(data, dict):
            # data is sparse dict
            self._sparse_data = dict(data)
            if self._sparse_data:
                self.rows = max(i for i, _ in self._sparse_data.keys()) + 1
                self.cols = max(j for _, j in self._sparse_data.keys()) + 1
            else:
                self.rows = 0
                self.cols = 0
        else:
            # expect list-of-lists
            if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
                raise TypeError("Data harus berupa list of lists atau dict {(i,j): val}.")
            self.rows = len(data)
            self.cols = len(data[0]) if self.rows > 0 else 0
            # all rows must have same length
            if not all(len(row) == self.cols for row in data):
                raise ValueError("Semua baris harus memiliki jumlah kolom yang sama.")
            # build sparse dict
            for r, row in enumerate(data):
                for c, val in enumerate(row):
                    if val != 0:
                        self._sparse_data[(r, c)] = val
        # dense cache kept None until requested

    def get_value(self, row, col):
        return self._sparse_data.get((row, col), 0)

    @property
    def data(self):
        """Return dense representation (list of lists). Cached for performance."""
        if self._dense_cache is not None:
            return self._dense_cache
        dense = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for (r, c), v in self._sparse_data.items():
            dense[r][c] = v
        self._dense_cache = dense
        return self._dense_cache

    def __repr__(self):
        return f"SparseMatrix(rows={self.rows}, cols={self.cols}, nnz={len(self._sparse_data)})"

    def __str__(self):
        return "\n".join(" ".join(str(self.get_value(r, c)) for c in range(self.cols)) for r in range(self.rows))
