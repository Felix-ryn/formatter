def is_square(matrix):
    """
    Memeriksa apakah sebuah matriks adalah matriks persegi.
    """
    if not matrix or not isinstance(matrix, list):
        return False
    
    rows = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != rows:
            return False
            
    return True

def is_symmetric(matrix):
    """
    Memeriksa apakah sebuah matriks adalah matriks simetris.
    """
    if not is_square(matrix):
        return False
        
    n = len(matrix)
    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] != matrix[j][i]:
                return False
                
    return True
