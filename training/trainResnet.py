
def train_resnet():
    class ResNet(nn.Module):

        def __init__(self, block, layers, num_classes=1000):
            super().__init__()
            
            self.inplanes = 64

            self.conv1 = nn.Conv2d(3, self.inplanes, kernel_size=7, stride=2, padding=3,
                                bias=False)
            self.bn1 = nn.BatchNorm2d(self.inplanes)
            self.relu = nn.ReLU(inplace=True)
            self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
            
            self.layer1 = self._make_layer(block, 64, layers[0])
            self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
            self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
            self.layer4 = self._make_layer(block, 512, layers[3], stride=2)
            
            self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
            self.fc = nn.Linear(512 , num_classes)


        def _make_layer(self, block, planes, blocks, stride=1):
            downsample = None  
    
            if stride != 1 or self.inplanes != planes:
                downsample = nn.Sequential(
                    nn.Conv2d(self.inplanes, planes, 1, stride, bias=False),
                    nn.BatchNorm2d(planes),
                )

            layers = []
            layers.append(block(self.inplanes, planes, stride, downsample))
            
            self.inplanes = planes
            
            for _ in range(1, blocks):
                layers.append(block(self.inplanes, planes))

            return nn.Sequential(*layers)
        
        
        def forward(self, x):
            x = self.conv1(x)           # 224x224
            x = self.bn1(x)
            x = self.relu(x)
            x = self.maxpool(x)         # 112x112

            x = self.layer1(x)          # 56x56
            x = self.layer2(x)          # 28x28
            x = self.layer3(x)          # 14x14
            x = self.layer4(x)          # 7x7

            x = self.avgpool(x)         # 1x1
            x = torch.flatten(x, 1)     # remove 1 X 1 grid and make vector of tensor shape 
            x = self.fc(x)

            return x