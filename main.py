from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from add_module import *
from func_defs import *

import numpy as np

# Устанавливает главное окно и фон для графика
def set_window():
    # создаём главное окно
    window = QMainWindow()

    window.setWindowTitle("Графическое приложение")
    window.setFixedSize(1400, 700)
    window.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0," 
                         "stop:0 rgba(0, 182, 119, 255),stop:0.427447 rgba(41, 61, 132, 235)," 
                         "stop:1 rgba(187, 13, 142, 255));")
    window.setWindowIcon(QIcon("pictures/icon_new.jpg"))
    # добавляем фон для графика
    label = QLabel(window)
    label.resize(650, 650)
    label.move(725, 25)

    pixmap = QPixmap("pictures/back_pic.png")
    pixmap = pixmap.scaled(650, 650)

    label.setPixmap(pixmap)

    return window, label
    

# Делаем строку для ввода функции
def make_function_input(window):
    function_input = QLineEdit(window)
    
    function_input.resize(650, 60)
    function_input.move(25, 25)
    function_input.setFont(QFont("Arial", 28))
    function_input.setAlignment(Qt.AlignmentFlag(4))

    function_input.setMaxLength(33)
    function_input.setStyleSheet("background-color: rgba(0, 95, 141, 100);" 
                             "border: 1px solid rgba(255, 255, 255, 40);" 
                             "border-radius: 7px;")
                             #"color: white;")
    function_input.setPlaceholderText("Ваша функция (a*x+x^b+x**c)")
    # function_input.setValidator(QRegularExpressionValidator(
    #     QRegularExpression(r'^((sin|cos|tan|cot|sec|csc|exp|log|sqrt)\s*\(\s*((-?\d+(\.\d+)?)|x)\s*\))$')))#r"^[0-9x*^/.()+-]+$"

    return function_input


# Делаем строки для ввода границ отрезка
def make_boundaries_input(window):
    # Создаём прозрачный текст для интерфейса с указанием на границы отрезка
    label = QLabel("Границы отрезка", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 24pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(250, 60)
    label.move(105, 80)
    # ввод начала отрезка
    start_section_line = QLineEdit(window)
    start_section_line.setFont(QFont("Ariel", 22))
    start_section_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                     "border: 1px solid rgba(255, 255, 255, 40);"
                                     "border-radius: 7px;")
    start_section_line.setMaxLength(11)
    start_section_line.resize(200, 60)
    start_section_line.move(30, 140)
    start_section_line.setPlaceholderText("a")
    start_section_line.setValidator(QRegularExpressionValidator(
        QRegularExpression(r"[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?")))
    # ввод конца отрезка
    end_section_line = QLineEdit(window)
    end_section_line.setFont(QFont("Ariel", 24))
    end_section_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                    "border: 1px solid rgba(255, 255, 255, 40);"
                                    "border-radius: 7px;")
    end_section_line.setMaxLength(11)
    end_section_line.resize(200, 60)
    end_section_line.move(245, 140)
    end_section_line.setPlaceholderText("b")
    end_section_line.setValidator(QRegularExpressionValidator(
        QRegularExpression(r"[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?")))

    return start_section_line, end_section_line


# Делаем строку для ввода шага
def make_step_input(window):
    # Создаём прозрачный текст для интерфейса с указанием на шаг разбиения
    label = QLabel("Шаг", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 24pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(200, 60)
    label.move(540, 80)
    # ввод для шага
    step_line = QLineEdit(window)
    step_line.setFont(QFont("Ariel", 22))
    step_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                            "border: 1px solid rgba(255, 255, 255, 40);"
                            "border-radius: 7px;")
    
    step_line.setMaxLength(11)
    step_line.resize(205, 60)
    step_line.move(470, 140)
    step_line.setPlaceholderText("step")
    step_line.setValidator(QRegularExpressionValidator(
        QRegularExpression(r"([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?")))

    return step_line


# Делаем строку для ввода количества операций
def make_max_count_input(window):
    # Создаём прозрачный текст для интерфейса с указанием на максимальное кол-во итераций
    label = QLabel("Макс. кол-во итераций", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
                        
    label.resize(340, 40)
    label.move(55, 205)
    # ввод для кол-во итераций
    max_count_line = QLineEdit(window)
    max_count_line.setFont(QFont("Ariel", 22))
    max_count_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                 "border: 1px solid rgba(255, 255, 255, 40);"
                                 "border-radius: 7px;")
    
    max_count_line.setMaxLength(6)
    max_count_line.resize(340, 60)
    max_count_line.move(30, 260)
    max_count_line.setPlaceholderText("Max count less 10^7")
    max_count_line.setValidator(QRegularExpressionValidator(
        QRegularExpression(r"[0-9]+")))

    return max_count_line


# Делаем строку для ввода погрешности счёта
def make_inaccur_input(window):
    # Создаём прозрачный текст для интерфейса с указанием на погрешность измерения
    label = QLabel("Погрешность измер.", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(285, 40)
    label.move(395, 205)
    # ввод для погрешности
    eps_line = QLineEdit(window)
    eps_line.setFont(QFont("Ariel", 22))
    eps_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);" 
                           "border: 1px solid rgba(255, 255, 255, 40);" 
                           "border-radius: 7px;")
    
    eps_line.setMaxLength(16)
    eps_line.resize(285, 60)
    eps_line.move(390, 260)
    eps_line.setPlaceholderText("eps (<1% (b-a))")
    eps_line.setValidator(QRegularExpressionValidator(
        QRegularExpression(r"^-?[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?$")))

    return eps_line


# Создание кнопок по положению, размеру с дефолтным стилем
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


# Создание таблицы для дальнейшего вывода корней
def make_table_output(window):

    table = QTableWidget(window)
    table.setFont(QFont("Ariel", 12))
    table.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                        "border: 1px solid rgba(255, 255, 255, 40);"
                        "border-radius: 7px;")
    table.resize(641, 245)
    table.move(25, 430)

    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    table.setColumnCount(6)

    header = table.horizontalHeader()
    header.setStyleSheet("background-color: lightblue; color: black;")
    header.setFont(QFont("Ariel", 16))

    table.setHorizontalHeaderLabels(["№ Корня", '[xi; x(i+1)]', 'x`', 'f(x`)', 'Итерации', 'Код работы'])

    return table


# Создание кнопок для программы с их связыванием с назначением
def make_buttons(window, label):
    prn_table = make_button(" Вывести \n таблицу ", window, 25, 340, 200, 70)
    prn_table.clicked.connect(lambda: print_table(table))

    prn_graph = make_button(" Вывести \n график ", window, 250, 340, 200, 70)
    prn_graph.clicked.connect(lambda: print_graph(label))

    del_data = make_button(" Удалить \n данные ", window, 475, 340, 200, 70)
    del_data.clicked.connect(delete_inputs)


# Функция для вывода в таблицу строки
def print_table(table):
    table.setRowCount(0)
    is_success, txt = check_data(1)
    if not is_success:
        return create_error(f"Ошибка в данных.\n{txt}", "input_error")
    
    start_val = float(bound_start.text())
    end_val = float(bound_end.text())
    step_val = float(step.text())
    my_function = function_input.text()
    my_function = my_function.replace("^", "**")
    eps_val = float(eps.text())
    mx_cnt_val = int(max_count.text())

    rc, val =  is_continuous(start_val, end_val, my_function)

    if not rc:
        return create_error(f"Ошибка при счёте функции\n в точке {val}", "error in counting result")


    x = gen_array(start_val, end_val, step_val)
    fst_bound = x[0]
    root_num = 0
    for snd_bound in x[1::]:
        if is_root(fst_bound, snd_bound, my_function):
            newton_rc, root, iters = simple_newton_for_bound(my_function, fst_bound, snd_bound, eps_val, mx_cnt_val)
            rc, f_root = cnt_func(root, my_function)
            if not rc:
                print(fst_bound, snd_bound)
                return create_error(f"Ошибка при счёте функции\n в точке {val}", "error in counting result")
            table.insertRow(root_num)
            table.setItem(root_num, 0, QTableWidgetItem(f'{root_num + 1}'))
            table.setItem(root_num, 1, QTableWidgetItem(f'[{fst_bound:.6}; {snd_bound:.6}]'))
            table.setItem(root_num, 2, QTableWidgetItem(f'{root:.6}'))
            table.setItem(root_num, 3, QTableWidgetItem(f'{f_root:.1e}'))
            table.setItem(root_num, 4, QTableWidgetItem(str(iters)))
            table.setItem(root_num, 5, QTableWidgetItem(str(newton_rc)))

            root_num += 1
        fst_bound = snd_bound
    if root_num == 0:
        create_error(f"На отрезке [{start_val:.4}; {end_val:.4}] не было\n обнаружено корней", "not roots")

# Функция, которая отчищает поля и таблицу
def delete_inputs():
    list_lines = [function_input, bound_start, bound_end, step, max_count, eps]
    for x in list_lines:
        x.setText("")
    table.setRowCount(0)


# Вывод графика с проверкой входных данных и результатов функции
def print_graph(label):
    is_success, txt = check_data(0)
    if not is_success:
        return create_error(f"Ошибка в данных.\n{txt}", "input_error")
    
    start_val = float(bound_start.text())
    end_val = float(bound_end.text())
    step_val = float(step.text())
    my_function = str(function_input.text())
    my_function = my_function.replace("^", "**")

    rc, val =  is_continuous(start_val, end_val, my_function)

    if not rc:
        return create_error(f"Ошибка при счёте функции\n в точке {val}", "error in counting result")

    x = gen_array(start_val, end_val, step_val)
    y = function_output(x, my_function)

    fig = Figure(figsize=(6.5, 6.5))
    fig.set_facecolor("#947aab")

    ax = fig.add_subplot()
    ax.set_title(f"График функции {str(function_input.text())}\n" +
                 f"на отрезке [{start_val}; {end_val}]")
    ax.set_facecolor("#c2b9c9")
    ax.set_xlabel('Значения x')
    ax.set_ylabel('Значения y')

    ax.xaxis.label.set_fontsize(18)
    ax.yaxis.label.set_fontsize(12)

    ax.plot(x, y)
    ax.grid()

    canvas = FigureCanvasQTAgg(fig)

    layout = QVBoxLayout()

    layout.deleteLater()
    layout.addWidget(canvas)
    layout.addStretch(1)

    label.setLayout(layout)


# Запускает проверку параметром и проверку функции
def check_data(var):
    is_success, rc =  check_params_primary()
    if not is_success:
        return False, rc
    
    is_success, rc =  check_func_primary()
    if not is_success:
        return False, rc
    
    if var == 1:
        is_success, rc =  check_eps()
        if not is_success:
            return False, rc
        
        is_success, rc = check_iters_cnt()
        if not is_success:
            return False, rc
    return True, ''


# проверяет, все ли поля заполнены, и верно ли это логически
def check_params_primary():
    if len(bound_start.text()) == 0:
        return False, 'Не введено начало отрезка'
    if len(bound_end.text()) == 0:
        return False, 'Не введен конец отрезка'
    if len(step.text()) == 0:
        return False, 'Не введен шаг разбиения'
    
    try:
        st_val = float(bound_start.text())
        en_val = float(bound_end.text())
        step_val = float(step.text())
        

        if st_val >= en_val:
            return False, 'Границы отрезка (a >= b)'
        elif step_val <= 0:
            return False, 'Шаг разбиения (<=0)'
        elif (en_val - st_val) < step_val:
            return False, 'Шаг разбиения больше\nотрезка'
        return True, ''
    
    except ValueError:
        return False, 'Перевод данных'


# делает элементарную проверку на верность введённое функции
def check_func_primary():
    my_func = str(function_input.text())
    func_sym = 'x0123456789+-*^/().'
    func_trig = ['log', 'sin', 'cos', 'exp', 'tan']

    if len(my_func) == 0:
        return False, 'Не введена функция'
    for element in func_trig:
        my_func = my_func.replace(f"{element}", '')
    for element in func_sym:
        my_func = my_func.replace(f"{element}", '')

    if len(my_func) > 0:
        return False, 'Функция неправильна'
    
    return True, ''


# делает проверку на то, что погрешность измерения хотя бы меньше 1%, чем длина отрезка
def check_eps():
    if len(eps.text()) == 0:
        return False, 'Не введена погрешность' 
    try:
        eps_val = float(eps.text())
        st_val = float(bound_start.text())
        en_val = float(bound_end.text())

        if (en_val - st_val) / 100 <= eps_val:
            return False, 'Погрешность >= 1% от отрезка'
    except ValueError:
        return False, 'Перевод погрешности'
    return True, ''


# проверка, введено ли максимальное кол-во итераций для вычисления корней
def check_iters_cnt():
    if len(max_count.text()) == 0:
        return False, 'Не введено макс. кол-во итераций'
    try:
        mx_iters_val = int(max_count.text())

        if mx_iters_val < 10:
            return False, 'Сомнительное кол-во операций'
    except ValueError:
        return False, 'Перевод максимального кол-во итераций'
    return True, ''


# функция для создания ошибки
def create_error(text, head):
    # окно ошибка
    error = QDialog(window)
    error.setWindowTitle(head)
    error.setFixedSize(300, 110)
    error.setStyleSheet("background-color: rgba(103, 59, 125, 200); border-radius: 4px;")
    # текст ошибки
    text_er = QLabel(error)
    text_er.setStyleSheet("background-color: none; border-radius: 4px;")
    text_er.setText(text)
    text_er.move(5, 5)
    text_er.setFont(QFont("Arial", 16))
    # кнопка ошибка
    button_exit = QPushButton("ОК", error)
    button_exit.setFont(QFont("Arial", 18))
    button_exit.setStyleSheet(u"color: black;\n"
                        "font-size: 22pt;\n"
                        "background-color: rgba(255, 255, 255, 100);\n"
                        "border: 1px solid rgba(255, 255, 255, 40);")
    button_exit.setGeometry(QRect(105, 70, 90, 40))
    button_exit.clicked.connect(error.done)
    # запуск ошибки
    error.exec()


app = QApplication([])

# Создание приложения
window, label = set_window()

# Создания элементов интерфейса для взаимодействия
function_input = make_function_input(window)
bound_start, bound_end = make_boundaries_input(window)
step = make_step_input(window)
max_count = make_max_count_input(window)
eps = make_inaccur_input(window)
table = make_table_output(window)

# Создание кнопок для работы
make_buttons(window, label)

# # Дополнительная функция для себя
# make_sound(window)

window.show()
app.exec()
