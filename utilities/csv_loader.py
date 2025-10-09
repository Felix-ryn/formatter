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

from ..matrix import Matrix
from ..sparsematrix import SparseMatrix

Number = Union[int, float]

def _to_number_if_possible(s: str) -> Optional[Number]:
    s = s.strip()
    if s == "":
        return None
    # coba int dulu
    try:
        v = int(s)
        return v
    except ValueError:
        try:
            v = float(s)
            return v
        except ValueError:
            return None

def _is_column_numeric(col_values: List[str]) -> bool:
    # kolom numeric jika setidaknya satu non-empty dan semua non-empty bisa diubah ke number
    non_empty = [v for v in col_values if v.strip() != ""]
    if not non_empty:
        return False
    for v in non_empty:
        if _to_number_if_possible(v) is None:
            return False
    return True

def _parse_rows(path: str, delimiter: Optional[str], skip_header: bool) -> (List[str], List[List[str]]):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, newline='') as f:
        reader = csv.reader(f, delimiter=delimiter) if delimiter else csv.reader(f)
        rows = list(reader)
    if not rows:
        return [], []
    header = []
    start = 0
    if skip_header:
        header = [h.strip() for h in rows[0]]
        start = 1
    data_rows = [r for r in rows[start:] if any(cell.strip() != "" for cell in r)]
    # ensure rectangular by padding empties to same length as first row
    maxlen = max((len(r) for r in data_rows), default=0)
    data_rows = [r + [""]*(maxlen - len(r)) for r in data_rows]
    return header, data_rows

def _select_columns_by_names_or_indices(header: List[str], selected: Optional[Iterable[Union[int,str]]]) -> List[int]:
    if not selected:
        return list(range(len(header))) if header else []
    sel_indices = []
    for s in selected:
        if isinstance(s, int):
            sel_indices.append(s)
        else:
            # string: try to find in header
            if s in header:
                sel_indices.append(header.index(s))
            else:
                raise ValueError(f"Selected column name '{s}' not found in header.")
    return sel_indices

def _convert_and_impute(columns: List[List[str]], strategy: str) -> List[Optional[List[Number]]]:
    numeric_cols = []
    for col in columns:
        # convert to numbers or None
        conv = [_to_number_if_possible(v) for v in col]
        numeric_cols.append(conv)

    # imputasi per kolom
    result = []
    for conv in numeric_cols:
        non_null = [v for v in conv if v is not None]
        if strategy == "drop":
            if any(v is None for v in conv):
                # drop entire column by signalling with None
                result.append(None)
                continue
        fill = 0
        if strategy == "zero":
            fill = 0
        elif strategy == "mean":
            fill = statistics.mean(non_null) if non_null else 0
        elif strategy == "median":
            fill = statistics.median(non_null) if non_null else 0
        else:
            raise ValueError(f"Unknown impute strategy: {strategy}")

        filled = [ (v if v is not None else fill) for v in conv ]
        # If all entries are int-like, cast to int when possible
        casted = []
        for x in filled:
            if isinstance(x, float) and abs(x - int(x)) < 1e-9:
                casted.append(int(round(x)))
            else:
                casted.append(x)
        result.append(casted)
    return result

def _transpose(cols: List[List[Number]]) -> List[List[Number]]:
    if not cols:
        return []
    nrows = len(cols[0])
    ncols = len(cols)
    rows = [[cols[c][r] for c in range(ncols)] for r in range(nrows)]
    return rows

def _minmax_scale(cols: List[List[Number]]) -> List[List[Number]]:
    scaled = []
    for col in cols:
        if not col:
            scaled.append(col)
            continue
        mn = min(col)
        mx = max(col)
        if mx == mn:
            scaled.append([0.0 for _ in col])
        else:
            scaled.append([ (x - mn) / (mx - mn) for x in col ])
    return scaled

def _zscore_scale(cols: List[List[Number]]) -> List[List[Number]]:
    scaled = []
    for col in cols:
        if not col:
            scaled.append(col)
            continue
        mu = statistics.mean(col)
        stdev = statistics.pstdev(col)
        if stdev == 0:
            scaled.append([0.0 for _ in col])
        else:
            scaled.append([ (x - mu) / stdev for x in col ])
    return scaled

def load_matrix_from_csv(
    path: str,
    delimiter: Optional[str] = None,
    skip_header: bool = False,
    selected_columns: Optional[Iterable[Union[int,str]]] = None,
    drop_non_numeric: bool = True,
    impute_strategy: str = "zero",   # "zero" | "mean" | "median" | "drop"
    normalize: Optional[str] = None, # None | "minmax" | "zscore"
    as_sparse: bool = False,
    sparse_threshold: float = 0.5
) -> Union[Matrix, SparseMatrix]:
    """
    Baca CSV dan kembalikan Matrix atau SparseMatrix yang telah diproses.
    - selected_columns: iterable of column indices or names (names hanya jika skip_header=True)
    - drop_non_numeric: jika True akan membuang kolom non-numerik (lainnya error)
    """
    header, data_rows = _parse_rows(path, delimiter, skip_header)
    if not data_rows:
        return Matrix([]) if not as_sparse else SparseMatrix({})

    ncols = len(data_rows[0])
    # build columns as strings
    cols = [ [row[c] if c < len(row) else "" for row in data_rows] for c in range(ncols) ]

    # select columns if requested
    if selected_columns:
        if skip_header:
            # allow name or index
            sel_indices = _select_columns_by_names_or_indices(header, selected_columns)
        else:
            # selected must be indices
            sel_indices = [int(x) for x in selected_columns]
        cols = [cols[i] for i in sel_indices]

    # detect numeric columns
    numeric_mask = [_is_column_numeric(col) for col in cols]

    if not all(numeric_mask):
        if drop_non_numeric:
            cols = [col for col, ok in zip(cols, numeric_mask) if ok]
            numeric_mask = [True]*len(cols)
        else:
            bad_idxs = [i for i,ok in enumerate(numeric_mask) if not ok]
            raise ValueError(f"Terdapat kolom non-numerik pada indeks: {bad_idxs}. Gunakan drop_non_numeric=True atau selected_columns untuk memilih kolom numerik.")

    # convert and impute
    converted_cols = _convert_and_impute(cols, impute_strategy)
    # _convert_and_impute may signal drop for columns -> remove those
    converted_cols = [c for c in converted_cols if c is not None]

    # normalize if requested
    if normalize == "minmax":
        converted_cols = _minmax_scale(converted_cols)
    elif normalize == "zscore":
        converted_cols = _zscore_scale(converted_cols)
    elif normalize is None:
        pass
    else:
        raise ValueError("normalize must be one of None, 'minmax', 'zscore'")

    # transpose to rows
    rows = _transpose(converted_cols)

    # decide sparse or dense
    total = len(rows) * (len(rows[0]) if rows else 0)
    zero_count = sum(1 for r in rows for v in r if v == 0)
    zero_ratio = (zero_count / total) if total > 0 else 0.0

    if as_sparse or zero_ratio >= sparse_threshold:
        sparse_dict = {}
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                if val != 0:
                    sparse_dict[(i, j)] = val
        return SparseMatrix(sparse_dict)
    else:
        return Matrix(rows)
