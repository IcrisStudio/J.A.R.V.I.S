import requests
from PIL import Image

url = "https://ai-api.magicstudio.com/api/ai-art-generator"

def generate_images(prompt):
    
    form_data = {
        "prompt": prompt
    }
    
    response = requests.post(url, data=form_data)
    
    if response.status_code == 200:
        with open("output.jpg", "wb") as output_file:
            output_file.write(response.content)
        print("Image generated and saved as 'output.jpg'.")
        open_image("output.jpg")
    else:
        print(f"Request failed with status code:{response.status_code}")
        
def open_image(image_path):
    try:
        img = Image.open(image_path)
        img.show()
    except FileNotFoundError:
        print(f"File {image_path} not found.")
        
        
