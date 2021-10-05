from db import engine
from src.init_bucket import init_bucket
from src.use_cases.add_soundtrack_to_video.soundtrack_adder import SoundtrackAdder


COMPOSITION_EXT = 'mp4'


class SavedVideoSoundtrackAdder:
    def __init__(self, soundtrack_adder: SoundtrackAdder):
        self.bucket = init_bucket()
        self.soundtrack_adder = soundtrack_adder

    def add_soundtrack_to_video(self, raw_video_id: str):
        self.raw_video_id = raw_video_id
        self.original_extension = self._get_original_extension()
        video_url = self.soundtrack_adder.add_soundtrack_to_video(self._get_original_video_url())
        mix_id = self._create_mix_db_record(video_url)
        return mix_id
    
    def _get_original_extension(self):
        return engine.execute(f"""
            SELECT `extension`
            FROM `raw_video`
            WHERE `raw_video_id` = {self.raw_video_id}""").scalar()
    
    def _get_original_video_url(self):
        extension = self.original_extension
        return f'https://storage.googleapis.com/en-hans/raw/{self.raw_video_id}.{extension}'

    def _create_mix_db_record(self, video_url):
        engine.execute(f'INSERT INTO `mix` (`raw_video_id`, `url`) VALUES ("{self.raw_video_id}", "{video_url}")')
        mix_id = engine.execute('SELECT LAST_INSERT_ID()').scalar()
        return str(mix_id)
