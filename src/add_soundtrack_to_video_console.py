from src.init_soundtrack_adder import init_soundtrack_adder
from src.use_cases.view_video_with_soundtrack.composition_src_loader import MixSrcLoader


def add_soundtrack_to_video_console(video_url: str):
    mix_id =  init_soundtrack_adder().add_soundtrack_to_video(video_url)
    print(MixSrcLoader().get_video_with_soundtrack(mix_id))
