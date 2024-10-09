import requests
from urllib.parse import urlencode
import pygame
from io import BytesIO

def speak(text):
    base_url = "https://murf.ai/Prod/anonymous-tts/audio"
    
    params = {
        "name": "en-UK-hazel",
        "text": text
    }
    
    encode_params = urlencode(params)
    
    url = f"{base_url}?{encode_params}"
    
    response = requests.get(url)
    
    pygame.mixer.init()
    pygame.mixer.music.load(BytesIO(response.content))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        

# speak("HEllo I AM JARVIS HOW CAN I HELP YOU TODAY")