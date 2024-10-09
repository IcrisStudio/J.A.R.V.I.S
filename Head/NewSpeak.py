from gtts import gTTS #pip install gtts
import pygame
import io
import time

def speak(text, lang="en"):
    tts = gTTS(text=text, tld='com.au', lang=lang, slow=False)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_fp, 'mp3')
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(1)
        
    pygame.mixer.music.stop()
    pygame.mixer.quit()

# speak("hello my name is jarvis")