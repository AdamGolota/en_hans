import sys

#from src.azure_emotion_recognizer.video_cutter import VideoCutter

#from src.add_soundtrack_to_video_console import add_soundtrack_to_video_console
from src.azure_emotion_recognizer.azure_emotion_recognizer import AzureEmotionRecognizer
from src.azure_emotion_recognizer.video_cutter import VideoCutter

# url = sys.argv[1]

# VideoCutter().get_several_frames('/Users/adamgolota/Downloads/adam_3.mp4', 3)

# AzureEmotionRecognizer().get_video_emotion('https://storage.googleapis.com/en-hans/Screenshot%20at%20Oct%2005%2021-47-14.png')
print(AzureEmotionRecognizer(
    VideoCutter()
).get_video_emotion('/Users/adamgolota/Downloads/vika_1.mp4'))

#add_soundtrack_to_video_console(url)
