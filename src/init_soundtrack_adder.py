import os
from src.playlist_suggester import CustomPlaylistSuggester
from src.emotion_recognizer import CVEmotionRecognizer
from src.music_generator import MubertMusicGenerator
from src.use_cases.add_soundtrack_to_video.soundtrack_adder import SoundtrackAdder


def init_soundtrack_adder():
    return SoundtrackAdder(
        emotion_recognizer=CVEmotionRecognizer(),
        playlist_suggester=CustomPlaylistSuggester(),
        music_generator=MubertMusicGenerator(),
    )
