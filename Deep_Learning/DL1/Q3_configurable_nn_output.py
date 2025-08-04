import random
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def relu(z):
    return max(0, z)

# User input
n = int(input('Enter number of inputs: '))
h = int(input('Enter number of hidden neurons: '))
activation = input('Enter activation (sigmoid/relu): ').strip().lower()

# Generate random inputs
inputs = [round(random.uniform(-1, 1), 2) for _ in range(n)]
print(f"Inputs: {inputs}")

# Hidden layer weights and biases
hidden_weights = [[round(random.uniform(-1, 1), 2) for _ in range(n)] for _ in range(h)]
hidden_biases = [round(random.uniform(-1, 1), 2) for _ in range(h)]
print(f"Hidden layer weights: {hidden_weights}")
print(f"Hidden biases: {hidden_biases}")

# Compute hidden layer outputs
hidden_outputs = []
for i in range(h):
    z = sum(inputs[j] * hidden_weights[i][j] for j in range(n)) + hidden_biases[i]
    if activation == 'sigmoid':
        out = sigmoid(z)
    elif activation == 'relu':
        out = relu(z)
    else:
        raise ValueError('Invalid activation function')
    hidden_outputs.append(round(out, 2))
print(f"Hidden outputs ({activation.capitalize()}): {hidden_outputs}")

# Output layer weights and bias
output_weights = [round(random.uniform(-1, 1), 2) for _ in range(h)]
output_bias = round(random.uniform(-1, 1), 2)
print(f"Output layer weights: {output_weights}")
print(f"Bias: {output_bias}")

# Compute final output (always use sigmoid for output)
z_out = sum(hidden_outputs[i] * output_weights[i] for i in range(h)) + output_bias
final_output = sigmoid(z_out)
print(f"Final Output: {round(final_output, 3)}")