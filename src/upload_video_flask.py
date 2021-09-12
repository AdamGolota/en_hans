import os
from src.use_cases.add_soundtrack_to_video import soundtrack_adder
from flask import request
from src.init_soundtrack_adder import init_soundtrack_adder
from src.use_cases.upload_video.video_uploader import Video, VideoUploader
from src.use_cases.view_video_with_soundtrack.composition_src_loader import CompositionSrcLoader


def upload_video_flask():
    video = request.files.get('video'),
    n, extension = os.path.splitext(request.files.get('video').filename)
    raw_video_id = VideoUploader().upload_video(Video(
        binary=video[0],
        extension=extension[1:]
    ))
    soundtrack_adder = init_soundtrack_adder()
    composition_id = soundtrack_adder.add_soundtrack_to_video(raw_video_id)
    return {
        'src': CompositionSrcLoader().get_video_with_soundtrack(composition_id),
        'emotion': soundtrack_adder.emotion
    }

