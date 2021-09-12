import requests
import time
import math

from keys import MUBERT_PAT

class MubertMusicGenerator:
    def generate_music(self, channel, duration):
        res = requests.post('https://api-b2b.mubert.com/v2/RecordTrack', json={
            "method":"RecordTrack",
            "params": {
                "pat": MUBERT_PAT,
                "playlist":"0.2.3", "duration": math.ceil(duration),
                "format":"mp3", "intensity":"medium",
                "bitrate":"32",
                "mode":"track"
            }
        })
        while not self._track_is_ready:
            time.sleep(1)
            print('track not ready yet')
        return res.json()['data']['tasks'][0]['download_link']

    @property
    def _track_is_ready(self):
        res = requests.post('https://api-b2b.mubert.com/v2/TrackStatus', json={
            "method":"TrackStatus",
            "params": {
                "pat": MUBERT_PAT
            }
        })
        tasks = res.json()['data']['tasks']
        last_task = tasks[len(tasks) - 1]
        return last_task['task_status_code'] == 2
