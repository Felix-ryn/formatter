# matrix.py
from validators.is_square import is_square
from validators.is_symmetric import is_symmetric
from validators.is_identity import is_identity

class Matrix:
    """
    Kelas untuk merepresentasikan objek matriks.
    """
    def __init__(self, data):
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise TypeError("Data harus berupa list of lists.")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0
        if not all(len(row) == self.cols for row in data):
            raise ValueError("Semua baris harus memiliki jumlah kolom yang sama.")

    def is_square(self):
        """Periksa apakah matriks persegi."""
        return is_square(self.data)

    def is_symmetric(self):
        """Periksa apakah matriks simetris."""
        return is_symmetric(self.data)

    def is_identity(self):
        """Periksa apakah matriks identitas."""
        return is_identity(self.data)

    def __repr__(self):
        return f"Matrix(rows={self.rows}, cols={self.cols})"

    def __str__(self):
        return "\n".join(" ".join(map(str, row)) for row in self.data)
