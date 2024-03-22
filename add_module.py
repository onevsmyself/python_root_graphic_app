from PyQt6.QtCore import QUrl, QDir
from PyQt6.QtMultimedia import *


def make_sound(window):
    player = QMediaPlayer()
    audio = QAudioOutput(window)
    player.setAudioOutput(audio)
    def restart_playback(status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            player.setPosition(0)
            player.play()

    player.mediaStatusChanged.connect(restart_playback)
    
    fullpath = QDir.current().absoluteFilePath("music/music1.mp3")
    url = QUrl.fromLocalFile(fullpath)

    player.setSource(url)

    player.play()
    