from env import TEMP_FILES_DIR
from moviepy.editor import AudioFileClip, CompositeAudioClip, VideoFileClip
from moviepy.audio.fx.volumex import volumex
import requests
from db import engine
from src.init_bucket import init_bucket


COMPOSITION_EXT = 'mp4'


class SoundtrackAdder:
    def __init__(self, emotion_recognizer, playlist_suggester, music_generator):
        self.bucket = init_bucket()
        self.composition_id = None
        self.original_extension = None
        self.video_clip = None
        self.emotion = None
        self.emotion_recognizer = emotion_recognizer
        self.playlist_suggester = playlist_suggester
        self.music_generator = music_generator

    def add_soundtrack_to_video(self, raw_video_id: str):
        self.raw_video_id = raw_video_id
        self.original_extension = self._get_original_extension()
        self._download_original_video()
        self.emotion = self._get_video_emotion()
        self._generate_music(self.emotion)
        self._attach_music_to_original_video()
        self._create_new_soundtrack_db_record()
        self._upload_video_with_music()
        return self.composition_id

    def _download_original_video(self):
        blob = self.bucket.blob(self._get_original_video_filename())
        blob.download_to_filename(self._original_video_temp_filename)

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
        return requests.get(music_url).content

    def _attach_music_to_original_video(self):
        music_clip = AudioFileClip(self._music_temp_filename)
        music_clip = music_clip.fx(volumex, 0.75)
        composite_audio = CompositeAudioClip([self.video_clip.audio, music_clip]) if self.video_clip.audio else music_clip
        self.video_clip = self.video_clip.set_audio(composite_audio)
        self._save_composition()

    def _save_composition(self):
        # https://github.com/Zulko/moviepy/issues/586
        if self.video_clip.rotation in (90, 270):
            self.video_clip = self.video_clip.resize(self.video_clip.size[::-1])
            self.video_clip.rotation = 0
        self.video_clip.write_videofile(self._composition_temp_filename)

    def _create_new_soundtrack_db_record(self):
        engine.execute(f'INSERT INTO `soundtrack` (`raw_video_id`) VALUES ("{self.raw_video_id}")')
        composition_id = engine.execute('SELECT LAST_INSERT_ID()').scalar()
        self.composition_id = str(composition_id)

    def _upload_video_with_music(self):
        with open(self._composition_temp_filename, 'rb') as composition_file:
            blob = self.bucket.blob(f'with_music/{self.composition_id}.{COMPOSITION_EXT}')
            blob.upload_from_file(composition_file, content_type=f'video/{COMPOSITION_EXT}')

    def _get_original_video_length(self):
        self.video_clip = VideoFileClip(self._original_video_temp_filename)
        return self.video_clip.duration

    def _get_original_video_filename(self):
        extension = self.original_extension
        return f'raw/{self.raw_video_id}.{extension}'
    
    def _get_original_extension(self):
        return engine.execute(f"""
            SELECT `extension`
            FROM `raw_video`
            WHERE `raw_video_id` = {self.raw_video_id}""").scalar()

    @property
    def _original_video_temp_filename(self):
        return f'{TEMP_FILES_DIR}/en_hans_video-{self.raw_video_id}.{self.original_extension}'

    @property
    def _music_temp_filename(self):
        return f'{TEMP_FILES_DIR}/en_hans_music-{self.raw_video_id}.mp3'

    @property
    def _composition_temp_filename(self):
        return f'{TEMP_FILES_DIR}/en_hans_composition-{self.raw_video_id}.{COMPOSITION_EXT}'
