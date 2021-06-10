import torch
from torchvision import models
from PIL import Image
from torchvision import transforms
import json

def process_img():

    #Load model and set it to eval mode
    resnet = models.resnet101(pretrained=True)

    resnet.eval()

    #Load input image and make sure it is the right format
    input_image = Image.open("./static/js/img/tmp.jpg")

    if (input_image.format != 'JPEG'):
        temp_image = input_image.convert("RGB")
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

    #Use cuda if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        resnet.to('cuda')

    #Get raw confidence values
    with torch.no_grad():
        output = resnet(input_batch)

    #Flatten confidence values
    probabilities = torch.nn.functional.softmax(output[0], dim=0)

    #Read class names
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]

    #Get top categories per image
    top5_prob, top5_catid = torch.topk(probabilities, 5)

    #Format class names and probability values
    prob = []
    names = []
    for i in range(top5_prob.size(0)):
        val = (top5_prob[i].item())*100
        formatted = "{:.2f}".format(val)
        prob.append(formatted)
        names.append(categories[top5_catid[i]])
        print(categories[top5_catid[i]], formatted, "%")

    # Format data for JSON output
    data = {}
    data['names'] = names
    data['prob'] = prob
    json_data = json.dumps(data)
    return (json_data)