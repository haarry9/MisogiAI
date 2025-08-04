import math

# Get inputs
x1, x2 = map(float, input('Enter x1, x2: ').split())
w1, w2 = map(float, input('Enter w1, w2: ').split())
b = float(input('Enter bias: '))

# Calculate neuron output
z = x1 * w1 + x2 * w2 + b
def sigmoid(z):
    return 1 / (1 + math.exp(-z))

output = sigmoid(z)
print(f'Neuron output: {output:.3f}')