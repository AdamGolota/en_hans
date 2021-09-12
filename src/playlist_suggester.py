class CustomPlaylistSuggester:
    def suggest_playlist(self, emotion):
        emotion_to_playlist = {
            'Angry': '6.17.2',
            'Disgust': '0.10.0',
            'Fear': '0.8.0',
            'Happy': '0.11.0',
            'Sad': '0.3.0',
            'Surprise': '6.6.4',
            'Neutral': '2.2.0'
        }
        return emotion_to_playlist[emotion]
