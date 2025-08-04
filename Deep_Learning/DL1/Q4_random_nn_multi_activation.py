import numpy as np
import matplotlib.pyplot as plt

# Set random seed for reproducibility
np.random.seed(42)

# Activation functions
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return np.maximum(0, x)

def leaky_relu(x):
    return np.where(x > 0, x, 0.01 * x)

activations = {
    'Sigmoid': sigmoid,
    'Tanh': tanh,
    'ReLU': relu,
    'Leaky ReLU': leaky_relu
}

# Randomly generate network structure
n_inputs = np.random.randint(3, 7)
L = np.random.randint(1, 4)
hidden_neurons = [np.random.randint(2, 6) for _ in range(L)]

# Print network structure
print(f"Random Seed: 42\n")
print(f"Generated Network:")
print(f"- Input Features: {n_inputs} → Values: ", end='')

# Generate input features
inputs = np.round(np.random.uniform(-10, 10, n_inputs), 2)
print(f"{list(inputs)}")
print(f"- Hidden Layers: {L}")
for i, n in enumerate(hidden_neurons):
    print(f"  • Layer {i+1}: {n} neurons")
print(f"- Output Layer: 1 neuron\n")

# Generate weights and biases for all layers
layer_sizes = [n_inputs] + hidden_neurons + [1]
weights = []
biases = []
for i in range(len(layer_sizes) - 1):
    w = np.round(np.random.uniform(-1, 1, (layer_sizes[i+1], layer_sizes[i])), 2)
    b = np.round(np.random.uniform(-1, 1, (layer_sizes[i+1],)), 2)
    weights.append(w)
    biases.append(b)
    print(f"Weights for Layer {i+1}:\n{w}")
    print(f"Biases for Layer {i+1}: {b}\n")

def forward_pass(x, weights, biases, activation_fn):
    a = x
    for w, b in zip(weights, biases):
        z = np.dot(w, a) + b
        a = activation_fn(z)
    return a[0] if a.shape == (1,) else a

# Compute final outputs for each activation function
final_outputs = {}
for name, fn in activations.items():
    out = forward_pass(inputs, weights, biases, fn)
    final_outputs[name] = np.round(float(out), 3)

print("Final Outputs:")
for name, val in final_outputs.items():
    print(f"- {name}: [{val}]")

# Plot final outputs
plt.bar(list(final_outputs.keys()), list(final_outputs.values()))
plt.ylabel('Final Output')
plt.title('Activation Function Output Comparison')
plt.show()