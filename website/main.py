from flask import Flask, render_template, request
from img_processor import process_img
import json

hostName = "localhost"
serverPort = 8080


app = Flask(__name__)

# Homepage redirect
@app.route("/", methods = ["GET", "POST"])
def main():
    return render_template('index.html')

# Image processing redirect
@app.route("/upload", methods = ["GET", "POST"])
def upload():

    # POST method for image upload
    if request.method == "POST":
        if request.files:

            image = request.files["fileImage"]
            print(image)
            if image.filename == "":
                print("blank img")
            else:
                image.save("./static/js/img/tmp.jpg")

    # GET method for sending JSON to webpage    
    else:
        json_data = process_img()
        print(json_data)
        with open('data.json', 'w') as f:
            json.dump(json_data, f)

        with open('data.json') as json_file:
            json_data = json.load(json_file)
        return json_data

    return render_template('up.html')



if __name__ == "__main__":
    app.run(debug=True, host=hostName, port=8080)