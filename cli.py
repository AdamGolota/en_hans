import sys

from src.azure_emotion_recognizer.video_cutter import VideoCutter

from src.add_soundtrack_to_video_console import add_soundtrack_to_video_console
from src.azure_emotion_recognizer.azure_emotion_recognizer import AzureEmotionRecognizer

def get_several_frames():
    VideoCutter().get_several_frames('/Users/adamgolota/Downloads/adam_3.mp4', 3)

def get_video_emotion():
    print(AzureEmotionRecognizer(
        VideoCutter()
    ).get_video_emotion('/Users/adamgolota/Downloads/vika_1.mp4'))

def add_soundtrack_to_video():
    # url = sys.argv[1]
    add_soundtrack_to_video_console('https://storage.googleapis.com/en-hans/vika_1.mp4')


add_soundtrack_to_video()
