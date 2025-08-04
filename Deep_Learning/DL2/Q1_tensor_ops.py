import torch

# 1. Create two random tensors
A = torch.randn(3, 2)
B = torch.randn(2, 3)

# 2. Matrix multiplication
C = A @ B

# 3. Element-wise addition
D = A + torch.ones_like(A)

# 4. Move result to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
C = C.to(device)

# 5. Print results
print(f"A: {A}")
print(f"B: {B}")
print(f"C: {C}")
print(f"C is on device: {C.device}")
print(f"D: {D}")