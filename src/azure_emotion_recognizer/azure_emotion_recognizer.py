from io import BytesIO, FileIO
import numpy as np
from typing import Dict, List
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import Emotion
from msrest.authentication import CognitiveServicesCredentials
from src.azure_emotion_recognizer.video_cutter import VideoCutter
from src.use_cases.add_soundtrack_to_video.emotion_recognizer import \
    EmotionRecognizer

from env import AZURE_KEY


ENDPOINT = 'https://en-hans.cognitiveservices.azure.com/'

POSSIBLE_EMOTIONS = ['anger', 'contempt', 'disgust', 'fear',
                     'happiness', 'neutral', 'sadness', 'surprise']

NUMBER_OF_FRAMES_TO_ANALYZE = 3

class AzureEmotionRecognizer(EmotionRecognizer):
    def __init__(self, video_cutter: VideoCutter) -> None:
        self.video_cutter = video_cutter
        self.face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

    def get_video_emotion(self, video_path: str):
        frame_filenames = self.video_cutter.get_several_frames(video_path,
                                                               NUMBER_OF_FRAMES_TO_ANALYZE)
        image_emotions = []
        for frame_filename in frame_filenames:
            with open(frame_filename, "rb") as frame:
                image_emotions += self._get_faces_emotion_percentages(frame)
        if not image_emotions:
            return None
        return self._get_strongest_emotion(self._emotions_matrix_sum(image_emotions))

    def _get_faces_emotion_percentages(self, image_stream: FileIO) -> List[Dict]:
        detected_faces = self.face_client.face.detect_with_stream(
            image_stream,
            return_face_attributes=['emotion']
        )
        return [self._emotion_percentage_to_array(face.face_attributes.emotion) for face
                                                                               in detected_faces]

    def _emotion_percentage_to_array(self, azure_emotion: Emotion):
        emotion_percentage_array = []
        for emotion in POSSIBLE_EMOTIONS:
            emotion_percentage_array.append(getattr(azure_emotion, emotion))
        return emotion_percentage_array

    def _emotions_matrix_sum(self, matrix: List[List[float]]):
        return np.matrix(matrix).sum(axis=0).tolist()[0]

    def _get_strongest_emotion(self, emotion_vector: List[float]):
        strongest_emotion_index = emotion_vector.index(max(emotion_vector))
        return POSSIBLE_EMOTIONS[strongest_emotion_index]
