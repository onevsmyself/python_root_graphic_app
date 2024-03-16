from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *


def set_window():
    window.setWindowTitle("Графическое приложение")
    window.setFixedSize(800, 700)
    window.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(0, 182, 119, 255)," 
                         "stop:0.427447 rgba(41, 61, 132, 235), stop:1 rgba(187, 13, 142, 255));")


def make_input_line(window):
    input_line = QLineEdit(window)
    
    input_line.resize(750, 80)
    input_line.move(25, 25)
    input_line.setFont(QFont("Arial", 34))
    input_line.setAlignment(Qt.AlignmentFlag(4))

    input_line.setMaxLength(36)
    input_line.setStyleSheet("background-color: rgba(0, 95, 141, 100);" 
                             "border: 1px solid rgba(255, 255, 255, 40);" 
                             "border-radius: 7px;")
    input_line.setPlaceholderText("Ваша функция")


def set_label_with_buttons(window):
    label = QLabel("Границы отрезка", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(230, 40)
    label.move(50, 120)

    start_section_line = QLineEdit(window)
    start_section_line.setFont(QFont("Ariel", 24))
    start_section_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                     "border: 1px solid rgba(255, 255, 255, 40);"
                                     "border-radius: 7px;")
    start_section_line.setMaxLength(6)
    start_section_line.resize(130, 45)
    start_section_line.move(30, 175)
    start_section_line.setPlaceholderText("a")

    end_section_line = QLineEdit(window)
    end_section_line.setFont(QFont("Ariel", 24))
    end_section_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                    "border: 1px solid rgba(255, 255, 255, 40);"
                                    "border-radius: 7px;")
    end_section_line.setMaxLength(6)
    end_section_line.resize(130, 45)
    end_section_line.move(170, 175)
    end_section_line.setPlaceholderText("b")

    label = QLabel("Шаг", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(60, 40)
    label.move(365, 120)

    step_line = QLineEdit(window)
    step_line.setFont(QFont("Ariel", 24))
    step_line.setStyleSheet("background-color: rgba(255, 255, 255, 30); border: 1px solid rgba(255, 255, 255, 40); border-radius: 7px;")
    step_line.setMaxLength(6)
    step_line.resize(145, 45)
    step_line.move(320, 175)
    step_line.setPlaceholderText("h")
    #----
    label = QLabel("Кол-во", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(160, 40)
    label.move(500, 120)

    step_line = QLineEdit(window)
    step_line.setFont(QFont("Ariel", 24))
    step_line.setStyleSheet("background-color: rgba(255, 255, 255, 30); border: 1px solid rgba(255, 255, 255, 40); border-radius: 7px;")
    step_line.setMaxLength(6)
    step_line.resize(130, 45)
    step_line.move(485, 175)
    step_line.setPlaceholderText("Nmax")
    #----
    label = QLabel("Погреш.", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(110, 40)
    label.move(640, 120)

    step_line = QLineEdit(window)
    step_line.setFont(QFont("Ariel", 24))
    step_line.setStyleSheet("background-color: rgba(255, 255, 255, 30); border: 1px solid rgba(255, 255, 255, 40); border-radius: 7px;")
    step_line.setMaxLength(6)
    step_line.resize(140, 45)
    step_line.move(635, 175)
    step_line.setPlaceholderText("eps")
  

def make_sound(window):
    player = QMediaPlayer()
    audio = QAudioOutput(window)
    player.setAudioOutput(audio)
    fullpath = QDir.current().absoluteFilePath("music/music2.mp3")
    url = QUrl.fromLocalFile(fullpath)
    player.setSource(url)

    return player




app = QApplication([])
window = QMainWindow()

set_window()
set_label_with_buttons(window)
input_line = make_input_line(window)

player = make_sound(window)
player.play()

window.show()
app.exec()