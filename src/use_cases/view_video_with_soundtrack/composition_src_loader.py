from db import engine
from src.use_cases.add_soundtrack_to_video.soundtrack_adder import COMPOSITION_EXT


class CompositionSrcLoader():
    def __init__(self):
        pass

    def get_video_with_soundtrack(self, composition_id: str):
        extension = self._get_extension(composition_id)
        return f'https://storage.cloud.google.com/en-hans/with_music/{composition_id}.{COMPOSITION_EXT}'

    def _get_extension(self, composition_id: str):
        return engine.execute(f"""
            SELECT `extension`
            FROM `raw_video`
            INNER JOIN `soundtrack` USING (`raw_video_id`)
            WHERE `soundtrack_id` = {composition_id}""").scalar()
