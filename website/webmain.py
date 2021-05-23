from flask import Flask, render_template, request
from main import process_img
import json

hostName = "localhost"
serverPort = 8080


app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def main():
    return render_template('index.html')

@app.route("/upload", methods = ["GET", "POST"])
def upload():

    if request.method == "POST":
        if request.files:

            image = request.files["fileImage"]
            print(image)
            if image.filename == "":
                print("blank img")
            else:
                image.save("./static/js/img/tmp.jpg")
                json_data = process_img()
                print(json_data)
                with open('data.json', 'w') as f:
                    json.dump(json_data, f)
    else:
        print ('why llmao')
        with open('data.json') as json_file:
            json_data = json.load(json_file)
        return json_data

    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)