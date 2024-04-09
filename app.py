from flask import Flask
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
import os

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/')
def hello():
    # Convert the PDF file to an image
    images = convert_from_path('test.pdf')

    # Extract the text from the image
    text = ""
    for image in images:
        text += image_to_string(image)

    # Return the extracted text
    return text


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
