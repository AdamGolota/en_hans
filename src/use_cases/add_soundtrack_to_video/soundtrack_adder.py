from time import sleep, time

import requests
from moviepy.audio.fx.volumex import volumex
from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip
from src.init_bucket import init_bucket
from src.use_cases.add_soundtrack_to_video.emotion_recognizer import \
    EmotionRecognizer
from env import TEMP_FILES_DIR

COMPOSITION_EXT = 'mp4'


class SoundtrackAdder:
    def __init__(self, emotion_recognizer: EmotionRecognizer, playlist_suggester, music_generator):
        self.bucket = init_bucket()
        self.original_video_url = None
        self.original_extension = 'mp4'
        self.video_clip = None
        self.emotion = None
        self.mix_id = None
        self.emotion_recognizer = emotion_recognizer
        self.playlist_suggester = playlist_suggester
        self.music_generator = music_generator

    def add_soundtrack_to_video(self, video_url: str):
        self.original_video_url = video_url
        self.mix_id = self._generate_timestamp_id()
        self._download_original_video()
        self.emotion = self._get_video_emotion()
        self._generate_music(self.emotion)
        self._attach_music_to_original_video()
        self._upload_video_with_music()
        return self.mix_id

    def _generate_timestamp_id(self):
        return int(time())

    def _download_original_video(self):
        with open(self._original_video_temp_filename, 'wb') as original_video_file:
            original_video_file.write(requests.get(self.original_video_url).content)

    def _get_video_emotion(self):
        emotion = self.emotion_recognizer.get_video_emotion(self._original_video_temp_filename)
        print(emotion)
        return emotion

    def _generate_music(self, emotion):
        playlist = self.playlist_suggester.suggest_playlist(emotion)
        length = self._get_original_video_length()
        music_url = self.music_generator.generate_music(playlist, length)
        with open(self._music_temp_filename, 'wb') as music_file:
            music_file.write(self._download_music(music_url))

    def _download_music(self, music_url):
        sleep(5)
        return requests.get(music_url).content

    def _attach_music_to_original_video(self):
        music_clip = AudioFileClip(self._music_temp_filename)
        music_clip = music_clip.fx(volumex, 0.75)
        composite_audio = (CompositeAudioClip([self.video_clip.audio, music_clip]) if self.video_clip.audio
                                                                                   else music_clip)
        self.video_clip = self.video_clip.set_audio(composite_audio)
        self._save_composition()

    def _save_composition(self):
        # https://github.com/Zulko/moviepy/issues/586
        if self.video_clip.rotation in (90, 270):
            self.video_clip = self.video_clip.resize(self.video_clip.size[::-1])
            self.video_clip.rotation = 0
        self.video_clip.write_videofile(self._composition_temp_filename)

    def _upload_video_with_music(self):
        with open(self._composition_temp_filename, 'rb') as composition_file:
            blob = self.bucket.blob(f'with_music/{self.mix_id}.{COMPOSITION_EXT}')
            blob.upload_from_file(composition_file, content_type=f'video/{COMPOSITION_EXT}')

    def _get_original_video_length(self):
        self.video_clip = VideoFileClip(self._original_video_temp_filename)
        return self.video_clip.duration

    @property
    def _original_video_temp_filename(self):
        return f'{TEMP_FILES_DIR}/en_hans_video-{self.mix_id}.{self.original_extension}'

    @property
    def _music_temp_filename(self):
        return f'{TEMP_FILES_DIR}/en_hans_music-{self.mix_id}.mp3'

    @property
    def _composition_temp_filename(self):
        return f'{TEMP_FILES_DIR}/en_hans_mix-{self.mix_id}.{COMPOSITION_EXT}'
