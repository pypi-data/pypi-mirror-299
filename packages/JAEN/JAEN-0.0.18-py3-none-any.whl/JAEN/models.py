import os
import torch
import torch.nn as nn

# CNN 모델 정의
class CNNModel(nn.Module):
    def __init__(self, pretrained=True, model_dir='data', model_file='models.pth'):
        super(CNNModel, self).__init__()
        
        # Convolutional Block (Conv -> Conv -> Pool -> Conv -> Conv -> Pool)
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # pool1
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)   # pool2
        )
        
        # Fully Connected Block (Flatten -> Linear -> Linear -> Linear)
        self.fc_layers = nn.Sequential(
            nn.Linear(256 * 7 * 7, 512),  # Flatten된 입력의 크기: 256 * 7 * 7
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 10)  # 10개의 클래스로 분류
        )
        
        # 사전 학습된 가중치를 불러올지 여부를 결정
        if pretrained:
            self.load_pretrained_weights(model_dir, model_file)

    def forward(self, x):
        x = self.conv_layers(x)          # Conv 블록을 통과
        x = x.view(x.size(0), -1)        # Flatten: FC에 넘기기 전 1차원 변환
        x = self.fc_layers(x)            # FC 블록을 통과
        return x

    # 사전 학습된 가중치 로드 함수
    def load_pretrained_weights(self, model_dir, model_file):
        model_path = os.path.join(model_dir, model_file)
        
        if os.path.exists(model_path):
            self.load_state_dict(torch.load(model_path))
            print("Pretrained weights loaded successfully.")
        else:
            raise FileNotFoundError(f"Model weights not found at {model_path}.")

# 모델 생성 및 가중치 로드
model = CNNModel(pretrained=True, model_dir='data', model_file='models.pth')
print(model)
