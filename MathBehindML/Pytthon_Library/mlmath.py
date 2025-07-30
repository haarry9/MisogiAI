"""
mlmath - A simple math library for machine learning basics.

Functions:
    dot_product(a, b) -> Computes the dot product of two vectors.
    matrix_multiply(A, B) -> Multiplies two matrices using nested loops.
    conditional_probability(events) -> Computes conditional probability P(A|B) = P(A ∩ B) / P(B).

Example:
    from mlmath import dot_product, matrix_multiply, conditional_probability

    print(dot_product([1,2,3], [4,5,6]))  # 32
"""

def dot_product(a, b):
    """
    Computes the dot product of two vectors.

    Args:
        a (list): First vector
        b (list): Second vector

    Returns:
        int/float: Dot product value

    Example:
        >>> dot_product([1,2,3], [4,5,6])
        32
    """
    return sum(x * y for x, y in zip(a, b))


def matrix_multiply(A, B):
    """
    Multiplies two matrices using nested loops (no NumPy).

    Args:
        A (list of lists): First matrix
        B (list of lists): Second matrix

    Returns:
        list of lists: Resultant matrix after multiplication

    Raises:
        ValueError: If matrix dimensions do not allow multiplication

    Example:
        >>> A = [[1, 2], [3, 4]]
        >>> B = [[5, 6], [7, 8]]
        >>> matrix_multiply(A, B)
        [[19, 22], [43, 50]]
    """
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError("Matrix dimensions do not allow multiplication")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result


def conditional_probability(events):
    """
    Computes conditional probability P(A|B) = P(A ∩ B) / P(B).

    Args:
        events (dict): Dictionary with keys:
                       'A_and_B' -> Probability of A and B
                       'B' -> Probability of B

    Returns:
        float: Conditional probability P(A|B)

    Raises:
        ValueError: If P(B) is 0

    Example:
        >>> conditional_probability({'A_and_B': 0.2, 'B': 0.5})
        0.4
    """
    P_B = events.get('B', 0)
    P_A_and_B = events.get('A_and_B', 0)

    if P_B == 0:
        raise ValueError("P(B) cannot be 0 for conditional probability")

    return P_A_and_B / P_B
