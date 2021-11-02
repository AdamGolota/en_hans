from src.azure_emotion_recognizer.azure_emotion_recognizer import AzureEmotionRecognizer
from src.azure_emotion_recognizer.video_cutter import VideoCutter
from src.playlist_suggester import CustomPlaylistSuggester
from src.music_generator import MubertMusicGenerator
from src.use_cases.add_soundtrack_to_video.soundtrack_adder import SoundtrackAdder


def init_soundtrack_adder():
    return SoundtrackAdder(
        emotion_recognizer=AzureEmotionRecognizer(VideoCutter()),
        playlist_suggester=CustomPlaylistSuggester(),
        music_generator=MubertMusicGenerator(),
    )
