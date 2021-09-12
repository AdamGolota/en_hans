"""Flask App
Тут инициализируется Flask приложение.
"""
import gc
from src.generate_audio_flask import generate_audio_flask
from flask import Flask

from src.upload_video_flask import upload_video_flask

app = Flask(__name__)

# ROUTES


@app.route('/upload-video', methods=['POST'])
def upload_video():
    res = upload_video_flask()
    gc.collect()
    return res


@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    return generate_audio_flask()

# @app.route('/video-with-soundtrack', methods=['GET'])
# def get_video_with_soundtrack():
#     return get_video_with_soundtrack_flask()
