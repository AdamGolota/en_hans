from src.use_cases.add_soundtrack_to_video.soundtrack_adder import COMPOSITION_EXT


class MixSrcLoader():
    def __init__(self):
        pass

    def get_video_with_soundtrack(self, mix_id: str):
        return f'https://storage.googleapis.com/en-hans/with_music/{mix_id}.{COMPOSITION_EXT}'
