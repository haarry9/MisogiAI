import torch
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# 1. Generate dataset and save to CSV
X, y = make_classification(n_samples=100, n_features=2, n_classes=2, random_state=1)
df = pd.DataFrame(X, columns=['f1', 'f2'])
df['label'] = y
df.to_csv('binary_data.csv', index=False)

# 2. Load dataset
X = torch.tensor(X, dtype=torch.float32)
y = torch.tensor(y, dtype=torch.float32).view(-1, 1)

# 3. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize weights and bias
w = torch.randn(2, 1, requires_grad=True)
b = torch.randn(1, requires_grad=True)

# 5. Sigmoid function
def sigmoid(x):
    return 1 / (1 + torch.exp(-x))

# 6. Binary cross-entropy loss
def bce_loss(y_pred, y_true):
    # Clamp to avoid log(0)
    y_pred = torch.clamp(y_pred, 1e-7, 1 - 1e-7)
    return -(y_true * torch.log(y_pred) + (1 - y_true) * torch.log(1 - y_pred)).mean()

# 7. Training loop
lr = 0.1
epochs = 30
for epoch in range(1, epochs + 1):
    # Forward pass
    logits = X_train @ w + b
    y_pred = sigmoid(logits)
    loss = bce_loss(y_pred, y_train)

    # Backward pass
    loss.backward()

    # Manual weight update
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
        w.grad.zero_()
        b.grad.zero_()

    if epoch == 1 or epoch % 5 == 0 or epoch == epochs:
        print(f"Epoch {epoch}: Loss = {loss.item():.4f}")

# 8. Evaluation
with torch.no_grad():
    logits = X_test @ w + b
    y_pred = sigmoid(logits)
    preds = (y_pred > 0.5).float()
    acc = (preds == y_test).float().mean().item() * 100
    print(f"Accuracy on test set = {acc:.1f}%")