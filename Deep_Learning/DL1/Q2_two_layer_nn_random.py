import random
import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

# Set random seed for reproducibility (optional, comment out for true randomness)
# random.seed(42)

# Generate random inputs
inputs = [round(random.uniform(-1, 1), 2) for _ in range(3)]
print(f"Inputs: {inputs}")

# First layer: 2 neurons, each with 3 weights and a bias
hidden_weights = [[round(random.uniform(-1, 1), 2) for _ in range(3)] for _ in range(2)]
hidden_biases = [round(random.uniform(-1, 1), 2) for _ in range(2)]
print(f"Hidden layer weights: {hidden_weights}")
print(f"Hidden layer biases: {hidden_biases}")

# Compute hidden layer outputs
hidden_outputs = []
for i in range(2):
    z = sum(inputs[j] * hidden_weights[i][j] for j in range(3)) + hidden_biases[i]
    out = sigmoid(z)
    hidden_outputs.append(round(out, 2))
print(f"Hidden outputs: {hidden_outputs}")

# Second layer: 1 neuron, 2 weights (one for each hidden neuron) and a bias
output_weights = [round(random.uniform(-1, 1), 2) for _ in range(2)]
output_bias = round(random.uniform(-1, 1), 2)
print(f"Output layer weights: {output_weights}")
print(f"Bias: {output_bias}")

# Compute final output
z_out = sum(hidden_outputs[i] * output_weights[i] for i in range(2)) + output_bias
final_output = sigmoid(z_out)
print(f"Final Output: {round(final_output, 3)}")