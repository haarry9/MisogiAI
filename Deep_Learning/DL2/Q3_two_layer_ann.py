import torch
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Load dataset (from CSV generated in Q2)
df = pd.read_csv('binary_data.csv')
X = torch.tensor(df[['f1', 'f2']].values, dtype=torch.float32)
y = torch.tensor(df['label'].values, dtype=torch.float32).view(-1, 1)

# 2. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Initialize weights and biases
W1 = torch.randn(2, 4, requires_grad=True)
b1 = torch.zeros(1, 4, requires_grad=True)
W2 = torch.randn(4, 1, requires_grad=True)
b2 = torch.zeros(1, 1, requires_grad=True)

# 4. Binary cross-entropy loss
def bce_loss(y_pred, y_true):
    y_pred = torch.clamp(y_pred, 1e-7, 1 - 1e-7)
    return -(y_true * torch.log(y_pred) + (1 - y_true) * torch.log(1 - y_pred)).mean()

# 5. Training loop
lr = 0.1
epochs = 30
for epoch in range(1, epochs + 1):
    # Forward pass
    Z1 = X_train @ W1 + b1
    A1 = torch.relu(Z1)
    Z2 = A1 @ W2 + b2
    Y_pred = torch.sigmoid(Z2)
    loss = bce_loss(Y_pred, y_train)

    # Backward pass
    loss.backward()

    # Manual weight update
    with torch.no_grad():
        W1 -= lr * W1.grad
        b1 -= lr * b1.grad
        W2 -= lr * W2.grad
        b2 -= lr * b2.grad
        W1.grad.zero_()
        b1.grad.zero_()
        W2.grad.zero_()
        b2.grad.zero_()

    if epoch == 1 or epoch % 5 == 0 or epoch == epochs:
        print(f"Epoch {epoch}: Loss = {loss.item():.4f}")

# 6. Evaluation
with torch.no_grad():
    Z1 = X_test @ W1 + b1
    A1 = torch.relu(Z1)
    Z2 = A1 @ W2 + b2
    Y_pred = torch.sigmoid(Z2)
    preds = (Y_pred > 0.5).float()
    acc = (preds == y_test).float().mean().item() * 100
    print(f"Accuracy: {acc:.1f}%")