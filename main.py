'''
Сделал Давидовский Кирилл Олегович. Группа ИУ7-24Б
2-ая лабораторная работа по питону.

Это приложение для вычисления корней функции на отрезке упрощённым методом Ньютона на PyQt6.
Программа на основании начала и конца отрезки, а также шага печатает график
с помощью библиотеки matplotlib. При дополнительном вводе максимального кол-ва операций и
погрешности, выводит таблицу. 
В таблице содержатся: 
1 - номер найденного корня, 
2 - элементарный отрезок, на котором был найден корень,
3 - приближённый аргумент из которого мы получили корень,
4 - значение функции при этом аргументе,
вычисленное по упрощённому методу Ньютона с заданной точностью,
5 - кол-во итераций, за которое было вычислено значение функции,
6 - код работы.

Коды работы:
0 - успешное нахождение корня, 
1 - невозможность посчитать корень, из-за несходимости 
(превышен установленный лимит максимального кол-ва итераций)
2 - невозможность посчитать корень, из-за деления на ноль
(по формуле упрощённому методу Ньютона нужно делить на производную в точке,
а она обратилась в ноль)
3 - данный корень может быть посчитан, но он лежит на начале элементарного отрезка
(по моей логике, этот корень должен принадлежать предыдущему элементарному отрезку,
чтобы не лежать в обоих) (a, b]

Также программа содержит меню с кнопкой для построения таблицы,
разными видами очистки, а также информацией о программе и её кодов работы
при печати таблицы.
'''


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from my_math import *


# Устанавливает главное окно и фон для графика
def set_window():
    # создаём главное окно
    window = QMainWindow()

    window.setWindowTitle("Приложение для уточнения корней")
    window.setFixedSize(1400, 750)
    window.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0," 
                         "stop:0 rgba(0, 182, 119, 255),stop:0.427447 rgba(41, 61, 132, 235)," 
                         "stop:1 rgba(187, 13, 142, 255));")
    window.setWindowIcon(QIcon("pictures/icon.jpg"))
    # добавляем фон для графика
    label = QLabel(window)
    label.resize(650, 650)
    label.move(725, 70)

    pixmap = QPixmap("pictures/back_pic.png")
    pixmap = pixmap.scaled(650, 650)

    label.setPixmap(pixmap)

    return window, label
    

# Создаёт меню для приложения, в котором есть расчёт таблицы, очистка полей и информация
def make_menu():
    bar = window.menuBar()
    bar.setFont(QFont("Arial", 20))
    bar.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0," 
                         "stop:0 rgba(51, 23, 194, 255),stop:0.427447 rgba(41, 61, 132, 235)," 
                         "stop:1 rgba(23, 194, 185, 255));")

    # создание действий, связанных с выводом
    output_table = QAction("Вывести таблицу", window)
    output_table.triggered.connect(lambda: print_table(table))
    output_graph = QAction("Вывести график", window)
    output_graph.triggered.connect(lambda: print_graph(label))
    # их привязка к пункту "Действия"
    actions = bar.addMenu("Действия")
    actions.setFont(QFont("Arial", 20))
    actions.addAction(output_table)
    actions.addAction(output_graph)

    # создание действия, связанных с отчисткой
    clear_inp = QAction("Отчистить поля ввода", window)
    clear_inp.triggered.connect(clear_inputs)
    clear_grp = QAction("Отчистить график", window)
    clear_grp.triggered.connect(clear_graph)
    clear_tab = QAction("Отчистить таблицу", window)
    clear_tab.triggered.connect(clear_table)
    clear_al = QAction("Отчистить всё", window)
    clear_al.triggered.connect(clear_all)
    # их привязка к пункту "Отчистка"
    clear = bar.addMenu("Отчистка")
    clear.setFont(QFont("Arial", 20))
    clear.addAction(clear_inp)
    clear.addAction(clear_grp)
    clear.addAction(clear_tab)
    clear.addAction(clear_al)

    # создание действия для вывода различной информации 
    # (запуск QMessageBox)
    about_app = QAction("Подробнее о приложении", window)
    about_app.triggered.connect(app_info_box.exec)
    about_rc = QAction("Коды работы программы", window)
    about_rc.triggered.connect(code_info_box.exec)
    # их привязка к пункту "Информация"
    info = bar.addMenu("Информация")
    info.setFont(QFont("Arial", 20))
    info.addAction(about_app)
    info.addAction(about_rc)


# для создания окно с информацией о программе
def make_message_boxes():
    app_info = QMessageBox(window)
    app_info.setWindowTitle("О приложении")   # заголовок
    app_info.setFont(QFont("Arial",14))   # шрифт
    app_info.setStyleSheet("background-color: rgb(143, 96, 173)")   # фоновый цвет
    app_info.setIcon(QMessageBox.Icon.Information)   # иконка
    app_info.setStandardButtons(QMessageBox.StandardButton.Close)   # кнопка
    app_info.setText("Приложение для уточнения корней, сделал\nДавидовский Кирилл, группа ИУ7-24Б.\n"
                     "Приложение было разработано при помощи библиотеки PyQt6. Оно вычисляет корни на "
                     "отрезке при помощи упрощённого метода Ньютона. А также строит график с локальными "
                     "экстремумами и корнями.\n\n"
                     "Для вычисления, заданный отрезок делится на элементарные отрезки с заданным шагом. "
                     "Также задаётся максимальное кол-во операций, для которых будут проведены " 
                     "вычисления.")

    code_info = QMessageBox(window)
    code_info.setWindowTitle("Коды работы программы")   # заголовок
    code_info.setFont(QFont("Arial",18))   # шрифт
    code_info.setStyleSheet("background-color: rgb(143, 96, 173)")   # фоновый цвет
    code_info.setIcon(QMessageBox.Icon.Information)   # иконка
    code_info.setStandardButtons(QMessageBox.StandardButton.Close)   # кнопка
    code_info.setText("0 - успешное нахождение корня. \n"
                      "1 - невозможность посчитать корень, из-за несходимости "
                      "(превышен установленный лимит максимального кол-ва итераций). \n"
                      "2 - невозможность посчитать корень, из-за деления на ноль "
                      "(по формуле упрощённому методу Ньютона нужно делить на производную в точке, "
                      "а она обратилась в ноль). \n"
                      "3 - данный корень может быть посчитан, но он лежит на начале элементарного отрезка "
                      "(по моей логике, этот корень должен принадлежать предыдущему элементарному отрезку, "
                      "чтобы не лежать в обоих) (a, b].")

    return app_info, code_info


# Делаем строку для ввода функции
def make_function_input():
    function_input = QLineEdit(window)
    
    function_input.resize(650, 60)
    function_input.move(25, 70)
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
def make_boundaries_input():
    # Создаём прозрачный текст для интерфейса с указанием на границы отрезка
    label = QLabel("Границы отрезка", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 24pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(250, 60)
    label.move(105, 125)
    # ввод начала отрезка
    start_section_line = QLineEdit(window)
    start_section_line.setFont(QFont("Ariel", 22))
    start_section_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                     "border: 1px solid rgba(255, 255, 255, 40);"
                                     "border-radius: 7px;")
    start_section_line.setMaxLength(11)
    start_section_line.resize(200, 60)
    start_section_line.move(30, 185)
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
    end_section_line.move(245, 185)
    end_section_line.setPlaceholderText("b")
    end_section_line.setValidator(QRegularExpressionValidator(
        QRegularExpression(r"[-+]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?")))

    return start_section_line, end_section_line


# Делаем строку для ввода шага
def make_step_input():
    # Создаём прозрачный текст для интерфейса с указанием на шаг разбиения
    label = QLabel("Шаг", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 24pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(200, 60)
    label.move(540, 125)
    # ввод для шага
    step_line = QLineEdit(window)
    step_line.setFont(QFont("Ariel", 22))
    step_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                            "border: 1px solid rgba(255, 255, 255, 40);"
                            "border-radius: 7px;")
    
    step_line.setMaxLength(11)
    step_line.resize(205, 60)
    step_line.move(470, 185)
    step_line.setPlaceholderText("step")
    step_line.setValidator(QRegularExpressionValidator(
        QRegularExpression(r"([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][-+]?[0-9]+)?")))

    return step_line


# Делаем строку для ввода количества операций
def make_max_count_input():
    # Создаём прозрачный текст для интерфейса с указанием на максимальное кол-во итераций
    label = QLabel("Макс. кол-во итераций", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
                        
    label.resize(340, 40)
    label.move(55, 250)
    # ввод для кол-во итераций
    max_count_line = QLineEdit(window)
    max_count_line.setFont(QFont("Ariel", 22))
    max_count_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                                 "border: 1px solid rgba(255, 255, 255, 40);"
                                 "border-radius: 7px;")
    
    max_count_line.setMaxLength(6)
    max_count_line.resize(340, 60)
    max_count_line.move(30, 305)
    max_count_line.setPlaceholderText("Max count less 10^7")
    max_count_line.setValidator(QRegularExpressionValidator(
        QRegularExpression(r"[0-9]+")))

    return max_count_line


# Делаем строку для ввода погрешности счёта
def make_inaccur_input():
    # Создаём прозрачный текст для интерфейса с указанием на погрешность измерения
    label = QLabel("Погрешность измер.", window)
    label.setStyleSheet(u"color: white;\n"
                        "font-size: 22pt;\n"
                        "background-color: none;\n"
                        "border: none;")
    label.resize(285, 40)
    label.move(395, 250)
    # ввод для погрешности
    eps_line = QLineEdit(window)
    eps_line.setFont(QFont("Ariel", 22))
    eps_line.setStyleSheet("background-color: rgba(255, 255, 255, 30);" 
                           "border: 1px solid rgba(255, 255, 255, 40);" 
                           "border-radius: 7px;")
    
    eps_line.setMaxLength(16)
    eps_line.resize(285, 60)
    eps_line.move(390, 305)
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
def make_table_output():

    table = QTableWidget(window)
    table.setFont(QFont("Ariel", 12))
    table.setStyleSheet("background-color: rgba(255, 255, 255, 30);"
                        "border: 1px solid rgba(255, 255, 255, 40);"
                        "border-radius: 7px;")
    table.resize(641, 245)
    table.move(25, 475)

    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    table.setColumnCount(6)

    header = table.horizontalHeader()
    header.setStyleSheet("background-color: lightblue; color: black;")
    header.setFont(QFont("Ariel", 16))

    table.setHorizontalHeaderLabels(["№ Корня", '[xi; x(i+1)]', 'x`', 'f(x`)', 'Итерации', 'Код работы'])

    return table


# Создание кнопок для программы с их связыванием с назначением
def make_buttons(window, label):
    prn_table = make_button(" Вывести \n таблицу ", window, 25, 385, 200, 70)
    prn_table.clicked.connect(lambda: print_table(table))

    prn_graph = make_button(" Вывести \n график ", window, 250, 385, 200, 70)
    prn_graph.clicked.connect(lambda: print_graph(label))

    del_data = make_button("Отчистить \n всё ", window, 475, 385, 200, 70)
    del_data.clicked.connect(clear_all)


# Функция для вывода в таблицу строки
def print_table(table: QTableWidget):
    is_success, txt = check_data(1)
    if not is_success:
        return create_error(f"Ошибка в данных.\n{txt}", "input_error")
    
    if table.rowCount() != 0:
        table.setRowCount(0)
    
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

    my_figure = Figure(figsize=(6.5, 6.5))
    my_figure.set_facecolor("#947aab")

    my_subplot = my_figure.add_subplot()
    my_subplot.set_title(f"График функции {str(function_input.text())}\n" +
                 f"на отрезке [{start_val}; {end_val}]")
    my_subplot.set_facecolor("#c2b9c9")
    my_subplot.set_xlabel('Значения x')
    my_subplot.set_ylabel('Значения y')

    my_subplot.xaxis.label.set_fontsize(18)
    my_subplot.yaxis.label.set_fontsize(12)

    x_extremes, y_extremes = get_locals_extremes(start_val, end_val, my_function)
    x_roots = get_roots(start_val, end_val, my_function)

    x = gen_array(start_val, end_val, step_val)
    y = function_output(x, my_function)

    my_subplot.plot(x, y, label=f'f(x) = {my_function}')

    my_subplot.scatter(x_extremes, y_extremes, color='blue', s=30, label='Найденные локальные экстремумы')
    my_subplot.scatter(x_roots, [0] * len(x_roots), color='red', s=30, label='Найденные корни')

    my_subplot.grid()
    my_subplot.legend(loc='best', prop={'size': 8})

    canvas = FigureCanvasQTAgg(my_figure)

    layout = QVBoxLayout()

    layout.deleteLater()
    layout.addWidget(canvas)
    layout.addStretch(1)

    label.setLayout(layout)


# Функция, которая отчищает всё
def clear_all():
    clear_inputs()
    clear_table()
    clear_graph()


# Функция, которая отчищает поля
def clear_inputs():
    list_lines = [function_input, bound_start, bound_end, step, max_count, eps]
    for x in list_lines:
        x.setText("")


# Функция, которая отчищает таблицу
def clear_table():
    table.setRowCount(0)


# Функция, которая отчищает график (на его место ставит пустой график)
def clear_graph():
    my_figure = Figure(figsize=(6.5, 6.5))
    my_figure.set_facecolor("#947aab")

    my_subplot = my_figure.add_subplot()
    my_subplot.plot([0], [0])
    my_subplot.grid()

    canvas = FigureCanvasQTAgg(my_figure)

    layout = QVBoxLayout()

    layout.deleteLater()
    layout.addWidget(canvas)
    layout.addStretch(1)

    label.setLayout(layout)


# разбиение на отрезки по шагу
def gen_array(start, end, step):
    array = []
    while start < end:
        array.append(start)
        start += step
    array.append(end)
    return array 


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
# Создания окна с информацией
app_info_box, code_info_box = make_message_boxes()
# Создание меню
make_menu()

# Создания элементов интерфейса для взаимодействия
function_input = make_function_input()
bound_start, bound_end = make_boundaries_input()
step = make_step_input()
max_count = make_max_count_input()
eps = make_inaccur_input()
table = make_table_output()

# Создание кнопок для работы
make_buttons(window, label)

window.show()
app.exec()
