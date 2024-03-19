from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np

from add_module import *

def set_window():
    window = QMainWindow()

    window.setWindowTitle("Графическое приложение")
    window.setFixedSize(1400, 700)
    window.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(0, 182, 119, 255)," 
                         "stop:0.427447 rgba(41, 61, 132, 235), stop:1 rgba(187, 13, 142, 255));")
    window.setWindowIcon(QIcon("pictures/icon_new.jpg"))

    label = QLabel(window)
    label.resize(600, 600)
    label.move(750, 50)

    pixmap = QPixmap("pictures/back_pic.png")
    pixmap = pixmap.scaled(600, 600)

    label.setPixmap(pixmap)

    return window, label
    

def make_function_line(window):
    input_line = QLineEdit(window)
    
    input_line.resize(650, 60)
    input_line.move(25, 25)
    input_line.setFont(QFont("Arial", 28))
    input_line.setAlignment(Qt.AlignmentFlag(4))

    input_line.setMaxLength(33)
    input_line.setStyleSheet("background-color: rgba(0, 95, 141, 100);" 
                             "border: 1px solid rgba(255, 255, 255, 40);" 
                             "border-radius: 7px;")
    input_line.setPlaceholderText("Ваша функция")
    input_line.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9xy^/*+-=().]*")))

    return input_line


def make_boundaries_input(window):
    label = QLabel("Границы отрезка", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 24pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(250, 60)
    label.move(100, 85)

    start_section_line = QLineEdit(window)
    start_section_line.setFont(QFont("Ariel", 24))
    start_section_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                     "border: 1px solid rgba(255, 255, 255, 40);"
                                     "border-radius: 7px;")
    start_section_line.setMaxLength(11)
    start_section_line.resize(200, 60)
    start_section_line.move(30, 150)
    start_section_line.setPlaceholderText("start")

    end_section_line = QLineEdit(window)
    end_section_line.setFont(QFont("Ariel", 24))
    end_section_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                    "border: 1px solid rgba(255, 255, 255, 40);"
                                    "border-radius: 7px;")
    end_section_line.setMaxLength(11)
    end_section_line.resize(200, 60)
    end_section_line.move(245, 150)
    end_section_line.setPlaceholderText("end")

    return start_section_line, end_section_line


def make_step_input(window):
    label = QLabel("Шаг", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 24pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(200, 60)
    label.move(535, 85)

    step_line = QLineEdit(window)
    step_line.setFont(QFont("Ariel", 24))
    step_line.setStyleSheet("background-color: rgba(255, 255, 255, 30); border: 1px solid rgba(255, 255, 255, 40); border-radius: 7px;")
    
    step_line.setMaxLength(6)
    step_line.resize(205, 60)
    step_line.move(470, 150)
    step_line.setPlaceholderText("step")

    return step_line


def make_max_count_input(window):
    label = QLabel("Макс. кол-во итераций", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(340, 40)
    label.move(50, 225)

    max_count_line = QLineEdit(window)
    max_count_line.setFont(QFont("Ariel", 24))
    max_count_line.setStyleSheet("background-color: rgba(255, 255, 255, 30); border: 1px solid rgba(255, 255, 255, 40); border-radius: 7px;")
    
    max_count_line.setMaxLength(6)
    max_count_line.resize(340, 60)
    max_count_line.move(30, 280)
    max_count_line.setPlaceholderText("Max count less 10^6")

    return max_count_line


def make_inaccur_input(window):
    label = QLabel("Погрешность измер.", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(285, 40)
    label.move(390, 225)

    eps_line = QLineEdit(window)
    eps_line.setFont(QFont("Ariel", 24))
    eps_line.setStyleSheet("background-color: rgba(255, 255, 255, 30); border: 1px solid rgba(255, 255, 255, 40); border-radius: 7px;")
    
    eps_line.setMaxLength(16)
    eps_line.resize(285, 60)
    eps_line.move(390, 280)
    eps_line.setPlaceholderText("eps")

    return eps_line
  

def make_button(text, window, x, y, width, height):
    button = QPushButton(text, window)
    button.setEnabled(True)
    button.setFixedSize(width, height)   # фиксируем размер
    button.move(x, y)   # ставим в позицию

    button.setFont(QFont("Arial", 22))
    button.setStyleSheet("background-color: rgba(0, 158, 142, 255);"
                         "border: 1px solid rgba(255, 255, 255, 40);"
                         "border-radius: 7px")
    return button

#######################
def make_table1_output(window):
    table = QLineEdit(window)
    table.setStyleSheet("background-color: rgba(255, 255, 255, 30); border: 1px solid rgba(255, 255, 255, 40); border-radius: 7px;")

    table.setEnabled(False)
    table.setMaxLength(100)
    table.resize(650, 190)
    table.move(25, 475)
    table.setPlaceholderText("Здесь будет ваша таблица")
    table.setAlignment(Qt.AlignmentFlag(5))
    return table

######################
def make_table_output(window):
    table = QTextEdit(window)
    table.setFont(QFont("Ariel", 20))
    table.setStyleSheet("background-color: rgba(255, 255, 255, 30); border: 1px solid rgba(255, 255, 255, 40); border-radius: 7px;")

    table.setEnabled(False)
    table.resize(650, 190)
    table.move(25, 475)
    table.setPlaceholderText("Здесь будет ваша таблица")
    table.setAlignment(Qt.AlignmentFlag(5))
    return table

def make_all_buttons(window, label):
    prn_table = make_button(" Вывести \n таблицу ", window, 25, 365, 200, 85)
    prn_table.clicked.connect(lambda: print_table(table))

    prn_graph = make_button(" Вывести \n график ", window, 250, 365, 200, 85)
    prn_graph.clicked.connect(lambda: print_graph(label))

    del_data = make_button(" Удалить \n данные ", window, 475, 365, 200, 85)
    del_data.clicked.connect(delete_inputs)



def print_table(table):
    work_in_table(table)


def check_data():
    step_val = float(step.text())
    st_val = float(bound_start.text())
    en_val = float(bound_end.text())

    if st_val >= en_val or step_val <= 0:
        return False
    return True


def print_graph(label):

    if not check_data():
        return

    fig = Figure(figsize=(6, 6))

    ax = fig.add_subplot()

    start_val = float(bound_start.text())
    end_val = float(bound_end.text())
    step_val = float(step.text())
    cnt_step = int((end_val - start_val) / step_val)

    x = np.linspace(start_val, end_val, cnt_step)
    y = np.power(x, 3)
    ax.set_xlabel('Значения x')
    ax.set_ylabel('Значения y')
    ax.plot(x, y)

    canvas = FigureCanvasQTAgg(fig)

    layout = QVBoxLayout()

    layout.deleteLater()
    layout.addWidget(canvas)
    layout.addStretch(1)

    label.setLayout(layout)


def delete_inputs():
    list_lines = [input_line, bound_start, bound_end, step, max_count, eps]
    for x in list_lines:
        x.setText("")


app = QApplication([])

window, label = set_window()

input_line = make_function_line(window)
bound_start, bound_end = make_boundaries_input(window)
step = make_step_input(window)
max_count = make_max_count_input(window)
eps = make_inaccur_input(window)
table = make_table_output(window)

make_all_buttons(window, label)

player = make_sound_player(window)
player.play()

window.show()
app.exec()