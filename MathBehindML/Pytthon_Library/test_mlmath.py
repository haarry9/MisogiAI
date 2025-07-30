from mlmath import dot_product, matrix_multiply, conditional_probability

# Test dot_product
print("Dot Product:", dot_product([1, 2, 3], [4, 5, 6]))

# Test matrix_multiply
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
print("Matrix Multiplication:", matrix_multiply(A, B))

# Test conditional_probability
events = {'A_and_B': 0.2, 'B': 0.5}
print("P(A|B):", conditional_probability(events))
