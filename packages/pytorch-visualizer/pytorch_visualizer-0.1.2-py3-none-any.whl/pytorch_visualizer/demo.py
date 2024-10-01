import torch.optim as optim
import torch.nn as nn
import torch
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from pytorch_visualizer.nn_visualizer import visualize

# Step 1: Create the make_moons dataset
X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert the data to PyTorch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.long)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.long)

# Step 2: Define a simple neural network model
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(2, 5)  # First layer (input: 2 features, output: 50 units)
        self.fc2 = nn.Linear(5, 3)
        self.fc3 = nn.Linear(3, 3)
        self.fc4 = nn.Linear(3, 2)   # Output layer (4, 2)
        self.relu = nn.ReLU()
        self.softmax = nn.LogSoftmax()
    
    @visualize(5, labels=y_train, loss_func='nllloss')
    def forward(self, x):
        x = self.fc1(x)  # Apply ReLU activation after first layer
        x = self.relu(x)
        x = self.fc2(x)              # Output layer (no activation, raw logits)
        x = self.fc3(x)
        x = self.fc4(x)
        x = self.softmax(x)
        #x = self.relu(x)
        #x = self.fc3(x)
        return x

# Step 3: Create the model, loss function, and optimizer
model = SimpleNN()
criterion = nn.CrossEntropyLoss()  # Cross-entropy loss for classification
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Step 4: Training loop (one sample at a time)
num_epochs = 1
for epoch in range(num_epochs):
    total_loss = 0.0
    for i in range(6):  # Iterate over each sample individually
        # Get one sample and its label
        input_sample = X_train[i]
        label = y_train[i]

        # Zero the gradients
        optimizer.zero_grad()

        # Forward pass
        output = model(input_sample)


        # Calculate loss
        loss = criterion(output, label)  # unsqueeze to match expected input for CrossEntropyLoss

        # Backward pass and optimization
        loss.backward()

        optimizer.step()

        total_loss += loss.item()
