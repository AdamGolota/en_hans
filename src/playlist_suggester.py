class CustomPlaylistSuggester:
    def suggest_playlist(self, emotion):
        emotion_to_playlist = {
            'Angry': '0.0.1',
            'Disgust': '0.0.1',
            'Fear': '0.0.1',
            'Happy': '0.0.1',
            'Sad': '0.0.1',
            'Surprise': '0.0.1',
            'Neutral': '0.0.1'
        }
        return emotion_to_playlist[emotion]
