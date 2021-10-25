from abc import ABC, abstractmethod


class EmotionRecognizer(ABC):
    @abstractmethod
    def get_video_emotion(self, video_path: str):
        pass
