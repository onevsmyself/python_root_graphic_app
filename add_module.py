from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *


def make_sound_player(window):
    player = QMediaPlayer()
    audio = QAudioOutput(window)

    player.setAudioOutput(audio)
    fullpath = QDir.current().absoluteFilePath("music/music2.mp3")
    url = QUrl.fromLocalFile(fullpath)

    player.setSource(url)
    return player


def work_in_table(table):
    text =  '+---+-----------+---------+---------+--------+----+\n'
    text += f'| № |[xi;x(i+1)]|x` ~ root|  f(x`)  |cnt_iter|err |\n'
    text += '+---+-----------+---------+---------+--------+----+'
    text += f'|---|-----------|---------|---------|--------|----|\n'
    text += '+---+-----------+---------+---------+--------+----+'
    table.setText(text)