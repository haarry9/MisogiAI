# Function to add two vectors
def add_vectors(a, b):
    return [x + y for x, y in zip(a, b)]

# Function to compute the dot product
def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

# Function to check if two vectors are orthogonal
def are_orthogonal(a, b):
    return dot_product(a, b) == 0

# Sample Input
a = [1, 2, 3]
b = [4, 5, 6]

# Output
print("Sum:", add_vectors(a, b))
print("Dot Product:", dot_product(a, b))
print("Orthogonal:", are_orthogonal(a, b))


# Function to multiply two matrices
def matrix_multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Check if multiplication is possible
    if cols_A != rows_B:
        raise ValueError("Matrix dimensions do not allow multiplication")

    # Initialize result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Multiply using nested loops
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

# Test matrices
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]

# Output
print("Matrix Multiplication Result:")
for row in matrix_multiply(A, B):
    print(row)
