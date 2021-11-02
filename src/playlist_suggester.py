class CustomPlaylistSuggester:
    def suggest_playlist(self, emotion):
        emotion_to_playlist = {
            'anger': '6.17.2',
            'disgust': '0.10.0',
            'contempt': '0.10.0',
            'fear': '0.8.0',
            'happiness': '0.11.0',
            'sadness': '0.3.0',
            'surprise': '6.6.4',
            'neutral': '2.2.0'
        }
        return emotion_to_playlist[emotion]
