
# Creating Pairs: Traditional `for` loop vs List comphrension!
pairs = []
for x in range(3):
    for y in range(2):
        pairs.append((x,y))

print(pairs)

pairs_comp = [(x,y) for x in range(4,6) for y in range(7,9)]
print(pairs_comp)

# Flattening a Matrix
matrix = [[1,2,3],[4,5,6],[7,8,9]]
flattened_matrix = []
for row in matrix:
    for num in row:
        flattened_matrix.append(num)

print(flattened_matrix)

matrix = [[1,2,3],[4,5,6],[7,8,9]]
flattened_matrix_comp = [num for row in matrix for num in row]
print(flattened_matrix_comp)
