import torch
from torchvision import transforms
from PIL import Image
from bot.config import MODEL_PATH, DEVICE

# Генератор
class Generator(torch.nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.model = torch.nn.Sequential(
            torch.nn.Conv2d(3, 64, kernel_size=4, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(128, 256, kernel_size=4, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),
            torch.nn.ReLU(),
            torch.nn.ConvTranspose2d(64, 3, kernel_size=4, stride=2, padding=1),
            torch.nn.Tanh(),
        )

    def forward(self, x):
        return self.model(x)

# Загрузка модели
generator = Generator().to(DEVICE)
generator.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE, weights_only=True))
generator.eval()

# Трансформации
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

# Обратные трансформации
inverse_transform = transforms.Compose([
    transforms.Normalize((-1, -1, -1), (2, 2, 2)),
    transforms.Lambda(lambda x: torch.clamp(x, 0, 1)),
    transforms.ToPILImage(),
])

# Функция стилизации
async def process_image(input_path):
    image = Image.open(input_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output_tensor = generator(input_tensor)
    output_image = inverse_transform(output_tensor.squeeze(0).cpu())
    return output_image



