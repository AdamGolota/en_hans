class CustomPlaylistSuggester:
    def suggest_playlist(self, emotion):
        emotion_to_playlist = {
            'Angry': '0.1.1',
            'Disgust': '0.4.0',
            'Fear': '0.10.0',
            'Happy': '0.0.1',
            'Sad': '0.3.0',
            'Surprise': '0.8.0',
            'Neutral': '2.0.0'
        }
        return emotion_to_playlist[emotion]
