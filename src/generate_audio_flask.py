import requests
import time
from env import TEMP_FILES_DIR
from datetime import datetime
from src.music_generator import MubertMusicGenerator


def generate_audio_flask():
    url = MubertMusicGenerator().generate_music('123', 15)
    res = requests.get(url)
    with open(f'{TEMP_FILES_DIR}/test-mubert-audio-{datetime.now()}.mp3', 'wb') as music_file:
        music_file.write(res.content)
    return ''
