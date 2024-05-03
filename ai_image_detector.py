import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder


class AIImageDetector(nn.Module):
    def __init__(self):
        super(AIImageDetector, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))

        x = x.view(-1, 128 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return x


def train_model(p_model, p_train_loader, p_criterion, p_optimizer, p_num_epochs=10):
    p_model.train()
    for epoch in range(p_num_epochs):
        running_loss = 0.0
        for images, labels in p_train_loader:
            p_optimizer.zero_grad()
            outputs = p_model(images)

            loss = p_criterion(outputs, labels)
            loss.backward()
            p_optimizer.step()

            running_loss += loss.item() * images.size(0)

        epoch_loss = running_loss / len(p_train_loader.dataset)
        print(f'Epoch [{epoch + 1}/{p_num_epochs}], Loss: {epoch_loss:.4f}')


def test_model(p_model, p_test_loader):
    p_model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in p_test_loader:
            outputs = p_model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = (correct / total) * 100
    print(f'Test Accuracy: {accuracy:.4f} %')


data_path = 'resources'

transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor()
])

# dataset = ImageFolder(root=data_path, transform=transform)
# train_size = int(0.8 * len(dataset))
# test_size = len(dataset) - train_size
#
# train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])
#
# train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
# test_loader = DataLoader(test_dataset, batch_size=32, shuffle=True)
#
# model = AIImageDetector()
# model.load_state_dict(torch.load("model.pth"))
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)
#
# train_model(model, train_loader, criterion, optimizer, p_num_epochs=10)
# test_model(model, test_loader)
# torch.save(model.state_dict(), 'model.pth')
