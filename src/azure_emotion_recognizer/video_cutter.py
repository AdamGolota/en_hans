from typing import Optional
from uuid import uuid1
from moviepy.editor import VideoFileClip
from env import TEMP_FILES_DIR


class VideoCutter:
    def __init__(self):
        self.clip: Optional[VideoFileClip] = None
        self.interval_between_frames = None
        self.number_of_frames = None

    def get_several_frames(self, video_filepath: str, number_of_frames: int):
        self.number_of_frames = number_of_frames
        self.clip = VideoFileClip(video_filepath)
        self.interval_between_frames = self._get_interval_between_frames()
        return self._save_frames_on_equal_intervals()

    def _save_frames_on_equal_intervals(self):
        frame_filenames = []
        for frame_index in range(self.number_of_frames):
            initial_offset = self.interval_between_frames / 2
            frame_time = initial_offset + self.interval_between_frames * frame_index
            frame_filename = self._save_frame(frame_time)
            frame_filenames.append(frame_filename)
        return frame_filenames

    def _save_frame(self, frame_time: float):
        frame_filename = f'{TEMP_FILES_DIR}/random_frame_{uuid1()}.jpg'
        self.clip.save_frame(frame_filename, frame_time)
        return frame_filename

    def _get_interval_between_frames(self):
        return self.clip.duration / self.number_of_frames
