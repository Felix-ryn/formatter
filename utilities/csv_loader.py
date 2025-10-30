# matriks/utilities/csv_loader.py
"""
Loader CSV yang mengubah CSV menjadi Matrix atau SparseMatrix.
Fitur:
 - detect kolom numerik otomatis (atau gunakan selected_columns)
 - skip header
 - imputasi: 'zero' | 'mean' | 'median' | 'drop'
 - normalisasi: None | 'minmax' | 'zscore'
 - opsi paksa as_sparse atau threshold otomatis
"""

from typing import List, Optional, Union, Iterable
import csv
import os
import statistics

from matrix import Matrix
from sparsematrix import SparseMatrix

# Tipe data untuk angka
Number = Union[int, float]

# ------------------------------------------------------------
# Fungsi bantuan: mencoba mengubah string menjadi angka jika memungkinkan
# ------------------------------------------------------------
def _to_number_if_possible(s: str) -> Optional[Number]:
    s = s.strip()
    if s == "":
        return None
    try:
        return int(s)    # coba konversi ke int
    except ValueError:
        try:
            return float(s)  # jika gagal, coba konversi ke float
        except ValueError:
            return None  # jika gagal juga, berarti bukan angka

# ------------------------------------------------------------
# Cek apakah kolom adalah kolom numerik
# ------------------------------------------------------------
def _is_column_numeric(col_values: List[str]) -> bool:
    # Ambil nilai yang tidak kosong
    non_empty = [v for v in col_values if v.strip() != ""]
    if not non_empty:
        return False
    # Jika setiap nilai tak kosong dapat dikonversi ke angka → kolom dianggap numerik
    return all(_to_number_if_possible(v) is not None for v in non_empty)

# ------------------------------------------------------------
# Membaca baris CSV dan memisahkan header jika ada
# ------------------------------------------------------------
def _parse_rows(path: str, delimiter: Optional[str], skip_header: bool):
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter) if delimiter else csv.reader(f)
        rows = list(reader)

    if not rows:
        return [], []

    header = []
    start = 0

    # Jika skip_header = True → baris pertama dianggap header
    if skip_header:
        header = [h.strip() for h in rows[0]]
        start = 1

    # Buang baris kosong
    data_rows = [r for r in rows[start:] if any(cell.strip() != "" for cell in r)]

    # Pastikan semua baris memiliki panjang yang sama
    maxlen = max((len(r) for r in data_rows), default=0)
    data_rows = [r + [""] * (maxlen - len(r)) for r in data_rows]

    return header, data_rows

# ------------------------------------------------------------
# Memilih kolom berdasarkan nama (jika header) atau indeks
# ------------------------------------------------------------
def _select_columns_by_names_or_indices(header: List[str], selected: Optional[Iterable[Union[int,str]]]) -> List[int]:
    if not selected:
        return list(range(len(header))) if header else []

    sel_indices = []
    for s in selected:
        if isinstance(s, int):
            sel_indices.append(s)
        else:
            if s in header:
                sel_indices.append(header.index(s))
            else:
                raise ValueError(f"Selected column name '{s}' not found in header.")
    return sel_indices

# ------------------------------------------------------------
# Konversi kolom ke angka + imputasi nilai kosong
# ------------------------------------------------------------
def _convert_and_impute(columns: List[List[str]], strategy: str) -> List[Optional[List[Number]]]:
    numeric_cols = [[_to_number_if_possible(v) for v in col] for col in columns]
    result = []

    for conv in numeric_cols:
        non_null = [v for v in conv if v is not None]

        # Jika strategi = drop dan ada nilai kosong → drop kolom
        if strategy == "drop" and any(v is None for v in conv):
            result.append(None)
            continue

        # Tentukan nilai pengganti (fill)
        if strategy == "zero":
            fill = 0
        elif strategy == "mean":
            fill = statistics.mean(non_null) if non_null else 0
        elif strategy == "median":
            fill = statistics.median(non_null) if non_null else 0
        else:
            raise ValueError(f"Unknown impute strategy: {strategy}")

        # Ganti nilai None dengan nilai imputasi
        filled = [v if v is not None else fill for v in conv]

        # Jika float tapi angkanya bulat → ubah ke int
        casted = [int(round(x)) if isinstance(x, float) and abs(x - int(x)) < 1e-9 else x for x in filled]
        result.append(casted)

    return result

# ------------------------------------------------------------
# Transpose kolom menjadi baris
# ------------------------------------------------------------
def _transpose(cols: List[List[Number]]) -> List[List[Number]]:
    if not cols:
        return []
    return [[cols[c][r] for c in range(len(cols))] for r in range(len(cols[0]))]

# ------------------------------------------------------------
# Normalisasi Min-Max
# ------------------------------------------------------------
def _minmax_scale(cols: List[List[Number]]) -> List[List[Number]]:
    scaled = []
    for col in cols:
        mn, mx = min(col), max(col)
        scaled.append([0.0 if mx == mn else (x - mn) / (mx - mn) for x in col])
    return scaled

# ------------------------------------------------------------
# Normalisasi Z-Score
# ------------------------------------------------------------
def _zscore_scale(cols: List[List[Number]]) -> List[List[Number]]:
    scaled = []
    for col in cols:
        mu = statistics.mean(col)
        stdev = statistics.pstdev(col)
        scaled.append([0.0 if stdev == 0 else (x - mu) / stdev for x in col])
    return scaled

# ------------------------------------------------------------
# Fungsi utama: Load CSV menjadi Matrix atau SparseMatrix
# ------------------------------------------------------------
def load_matrix_from_csv(
    path: str,
    delimiter: Optional[str] = None,
    skip_header: bool = False,
    selected_columns: Optional[Iterable[Union[int,str]]] = None,
    drop_non_numeric: bool = True,
    impute_strategy: str = "zero",
    normalize: Optional[str] = None,
    as_sparse: bool = False,
    sparse_threshold: float = 0.5
) -> Union[Matrix, SparseMatrix]:

    header, data_rows = _parse_rows(path, delimiter, skip_header)
    if not data_rows:
        return SparseMatrix({}) if as_sparse else Matrix([])

    # Bentuk kolom dari data
    cols = [[row[c] for row in data_rows] for c in range(len(data_rows[0]))]

    # Pilih kolom tertentu jika diminta
    if selected_columns:
        cols = [cols[i] for i in (_select_columns_by_names_or_indices(header, selected_columns) if skip_header else map(int, selected_columns))]

    # Deteksi kolom numerik
    numeric_mask = [_is_column_numeric(col) for col in cols]

    if not all(numeric_mask):
        if drop_non_numeric:
            cols = [col for col, ok in zip(cols, numeric_mask) if ok]
        else:
            raise ValueError("Terdapat kolom non-numerik. Gunakan drop_non_numeric=True atau pilih kolom secara manual.")

    # Konversi + imputasi
    converted_cols = [c for c in _convert_and_impute(cols, impute_strategy) if c is not None]

    # Normalisasi jika diminta
    if normalize == "minmax":
        converted_cols = _minmax_scale(converted_cols)
    elif normalize == "zscore":
        converted_cols = _zscore_scale(converted_cols)

    # Ubah orientasi → baris
    rows = _transpose(converted_cols)

    # Tentukan apakah perlu sparse
    total = len(rows) * len(rows[0])
    zero_ratio = sum(v == 0 for r in rows for v in r) / total if total else 0

    if as_sparse or zero_ratio >= sparse_threshold:
        return SparseMatrix({(i, j): v for i, r in enumerate(rows) for j, v in enumerate(r) if v != 0})
    return Matrix(rows)