from src.playlist_suggester import CustomPlaylistSuggester
from src.opensource_emotion_recognizer import OpensourceEmotionRecognizer
from src.music_generator import MubertMusicGenerator
from src.use_cases.add_soundtrack_to_video.soundtrack_adder import SoundtrackAdder


def init_soundtrack_adder():
    return SoundtrackAdder(
        emotion_recognizer=OpensourceEmotionRecognizer(),
        playlist_suggester=CustomPlaylistSuggester(),
        music_generator=MubertMusicGenerator(),
    )
