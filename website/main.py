import torch
from torchvision import models
from PIL import Image
from torchvision import transforms
import json

def process_img():
    resnet = models.resnet101(pretrained=True)

    resnet.eval()

    input_image = Image.open("./static/js/img/tmp.jpg")

    if (input_image.format != 'JPEG'):
        temp_image = input_image.convert("RGB")
        print(input_image.mode)
        temp_image.save('./static/js/img/tmp.jpg', quality=100)
        input_image = Image.open("./static/js/img/tmp.jpg")

    #Preprocessing
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    input_tensor = preprocess(input_image)

    input_batch = input_tensor.unsqueeze(0)

    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        resnet.to('cuda')

    with torch.no_grad():
        output = resnet(input_batch)

    #print(output[0])

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    #print(probabilities)



    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]
    # Show top categories per image
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    prob = []
    names = []
    for i in range(top5_prob.size(0)):
        val = (top5_prob[i].item())*100
        #val = val*100
        formatted = "{:.2f}".format(val)
        prob.append(formatted)
        names.append(categories[top5_catid[i]])
        print(categories[top5_catid[i]], formatted, "%")

    data = {}
    data['names'] = names
    data['prob'] = prob
    json_data = json.dumps(data)
    return (json_data)