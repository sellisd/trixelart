from flask import Flask, request, send_file, render_template, redirect
import requests
from PIL import Image
from io import BytesIO
from image_processing import pixelate_image_with_right_triangles
import base64
app = Flask(__name__)

def open_image_from_url(url):
    response = requests.get(url)
    print(f"Fetching URL: {url}")
    print(f"Response status code: {response.status_code}")
    img_data = BytesIO(response.content)
    return Image.open(img_data)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/pixelate', methods=['POST'])
def pixelate():
    url = request.form.get('url')
    triangle_size = int(request.args.get('size', 30))
    if not url:
        return "URL parameter is required", 400
    
    try:
        image = open_image_from_url(url)
        pixelated_img = pixelate_image_with_right_triangles(image, triangle_size)
        img_io = BytesIO()
        pixelated_img.save(img_io, 'PNG')
        img_io.seek(0)
        pixelated_img_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return render_template('result.html', pixelated_img_data=pixelated_img_data)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)