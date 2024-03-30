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
3 - возникла ошибка при счёте функции
4 - при счёте корень вышел из искомого отрезка
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
    output = QAction("Выполнить программу", window)
    output.triggered.connect(lambda: proc_work(table, label))
    # их привязка к пункту "Действия"
    actions = bar.addMenu("Действия")
    actions.setFont(QFont("Arial", 20))
    actions.addAction(output)

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


# для создания окон с информацией о программе и кодами работы
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
                     "вычисления.\n\n"
                     "Программа поддерживает следующие функции: "
                     "'log', 'sin', 'cos', 'exp', 'tan', 'sqrt', 'abs'. "
                     "А также 'e'.\nФункция записывается без указания 'y', "
                     "и без разделителей в виде пробелов.\n(x^3+12*x-sin(x))")

    code_info = QMessageBox(window)
    code_info.setWindowTitle("Коды работы программы")   # заголовок
    code_info.setFont(QFont("Arial",18))   # шрифт
    code_info.setStyleSheet("background-color: rgb(143, 96, 173)")   # фоновый цвет
    code_info.setIcon(QMessageBox.Icon.Information)   # иконка
    code_info.setStandardButtons(QMessageBox.StandardButton.Close)   # кнопка
    code_info.setText("0 - успешное нахождение корня. \n"
                      "1 - невозможность посчитать корень, из-за несходимости или особенности "
                      "упрощённого метода Ньютона, который может вылетать за границу отрезка "
                      "и отправиться в неизвестном направлении... "
                      "(превышен установленный лимит максимального кол-ва итераций). \n"
                      "2 - невозможность посчитать корень, из-за деления на ноль "
                      "(по формуле упрощённому методу Ньютона нужно делить на производную в точке, "
                      "а она обратилась в ноль). \n"
                      "3 - возникла ошибка при счёте функции.\n"
                      "4 - при счёте корня, функция вышли из отрезка. " 
                      "(Могло произойти из-за выбранного метода).")

    return app_info, code_info


# Делаем строку для ввода функции
def make_function_input():
    function_input = QLineEdit(window)
    
    function_input.resize(650, 60)
    function_input.move(25, 70)
    function_input.setFont(QFont("Arial", 28))
    function_input.setAlignment(Qt.AlignmentFlag(4))

    function_input.setMaxLength(100)
    function_input.setStyleSheet("background-color: rgba(0, 95, 141, 100);" 
                             "border: 1px solid rgba(255, 255, 255, 40);" 
                             "border-radius: 7px;")
                             #"color: white;")
    function_input.setPlaceholderText("Ваша функция (a*x+x^b+x**c)")

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
    # Создаём прозрачный текст для интерфейса
    # с указанием на максимальное кол-во итераций
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
    max_count_line.setPlaceholderText("Max count (>= 3)")
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

    table.setHorizontalHeaderLabels(["№ Корня", '[xi; x(i+1)]', 'x`',
                                    'f(x`)', 'Итерации', 'Код работы'])

    return table


# Создание кнопок для программы и их связыванием с назначением
def make_buttons(window, label):
    process = make_button(" Начать работу ", window, 25, 385, 325, 70)
    process.clicked.connect(lambda: proc_work(table, label))

    del_data = make_button("Отчистить всё ", window, 375, 385, 300, 70)
    del_data.clicked.connect(clear_all)


# Функция для работы программы, которая выводит таблицу и график
# а также проверяет возможность это сделать
def proc_work(table, label):
    my_start = bound_start.text()
    my_end = bound_end.text()
    my_step = step.text()
    my_eps = eps.text()
    my_mx_cnt = max_count.text()
    my_function = function_input.text()

    if check_data(my_start, my_end, my_step, my_eps, my_mx_cnt, my_function):
        start_val = float(my_start)
        end_val = float(my_end)
        step_val = float(my_step)
        eps_val = float(my_eps)
        mx_cnt_val = int(my_mx_cnt)
        my_function = my_function.replace("^", "**")

        roots_boundaries_list = find_ar_roots(start_val, end_val, step_val, my_function)
        info_matrix, ar_x_roots, ar_y_roots = make_info(roots_boundaries_list, my_function, eps_val, mx_cnt_val)
        x_extremes, y_extremes = get_locals_extremes(start_val, end_val, my_function)

        print_table(table, info_matrix)
        print_graph(label, ar_x_roots, ar_y_roots, start_val, end_val, my_function, x_extremes, y_extremes)
    

# Запускает проверку параметром и проверку функции
def check_data(my_start, my_end, my_step, my_eps, my_mx_cnt, my_function):
    if not check_boundaries(my_start, my_end):
        return False

    if not check_func_primary(my_function):
        return False

    if not check_step(float(my_start), float(my_end), my_step):
        return False
    
    if not check_eps(float(my_start), float(my_end), my_eps):
        return False

    if not check_iters_cnt(my_mx_cnt):
        return False

    if not check_continuous(float(my_start), float(my_end), my_function):
        return False

    return True


# находит отрезки, в которых лежит корень
def find_ar_roots(start_val, end_val, step_val, my_function):
    x = gen_array_with_step(start_val, end_val, step_val)
    fst_bound = x[0]
    root_num = 0

    roots_boundaries_list = []

    for snd_bound in x[1::]:
        # если корень на нужному отрезке, то начинаем запись в таблицу
        if is_root(fst_bound, snd_bound, my_function):
            roots_boundaries_list.append([fst_bound, snd_bound])
            root_num += 1
        fst_bound = snd_bound

    return roots_boundaries_list


# на основе отрезков, в которой лежит корень сделать дополнительную информацию
# для печати таблицы и графика
def make_info(roots_boundaries_list, my_function, eps_val, mx_cnt_val):
    matrix = []    
    root_num = 0

    ar_x_roots = []
    ar_y_roots = []

    for boundary in roots_boundaries_list:
        fst_bound = boundary[0]
        snd_bound = boundary[1]
        newton_rc, root, iters = simple_newton_for_bound(my_function, fst_bound, snd_bound, eps_val, mx_cnt_val)
        # проверка на то, что есть корень
        # получение значения функции для корня
        if root != '-':
            rc, f_root = cnt_func(root, my_function)

            if not rc:
                f_root = '-'
            else:
                f_root = f'{f_root:.1e}'

            root = f'{root:.5f}'
            ar_x_roots.append(float(root))
            ar_y_roots.append(float(f_root))
        else:
            f_root = '-'
        
        # преобразование границ отрезка
        str_fst_bound = f'{fst_bound:4.3f}'
        str_snd_bound = f'{snd_bound:4.3f}'
        # заполнение матрицы
        matrix.append([f'{root_num + 1}', f'[{str_fst_bound}; {str_snd_bound}]', root, f_root,
                       str(iters), str(newton_rc)])

        root_num += 1
    return matrix, ar_x_roots, ar_y_roots


# Заполняет таблицу данными
def print_table(table, matrix):
    if table.rowCount() != 0:
        table.setRowCount(0)

    index = 0

    for arr_info in matrix:
        table.insertRow(index)   # вставляем строчку для записи
        format_table(table)   # форматируем столбцы таблицы

        # заполнение текущей строки таблицы
        table.setItem(index, 0, QTableWidgetItem(arr_info[0]))
        table.setItem(index, 1, QTableWidgetItem(arr_info[1]))
        table.setItem(index, 2, QTableWidgetItem(arr_info[2]))
        table.setItem(index, 3, QTableWidgetItem(arr_info[3]))
        table.setItem(index, 4, QTableWidgetItem(arr_info[4]))
        table.setItem(index, 5, QTableWidgetItem(arr_info[5]))
        index += 1


# Делает формат столбцов в таблице
def format_table(table):
    header = table.horizontalHeader()
    header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
    header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
    header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)


# Вывод графика с проверкой входных данных и результатов функции
def print_graph(label, ar_x_roots, ar_y_roots, start_val, end_val, my_function, x_extremes, y_extremes): 
    # создание фигуры для графика
    my_figure = Figure(figsize=(6.5, 6.5))
    my_figure.set_facecolor("#947aab")
    # создание окна для работы
    my_subplot = my_figure.add_subplot()
    my_subplot.set_title(f"График функции {my_function}\n" +
                 f"на отрезке [{start_val}; {end_val}]")
    my_subplot.set_facecolor("#c2b9c9")
    my_subplot.set_xlabel('Значения x')
    my_subplot.set_ylabel('Значения f(x)')

    my_subplot.xaxis.label.set_fontsize(18)
    my_subplot.yaxis.label.set_fontsize(12)

    x = gen_array(start_val, end_val)
    y = function_output(x, my_function)
    # строим график функции
    my_subplot.plot(x, y, label=f'f(x) = {my_function}')

    # добавляем особые точки для экстремумов и корней
    my_subplot.scatter(x_extremes, y_extremes, color='blue', s=30, label='Найденные локальные экстремумы')
    my_subplot.scatter(ar_x_roots, ar_y_roots, color='red', s=30, label='Найденные корни')
    
    my_subplot.grid()   # создаём сетку
    my_subplot.legend(loc='best', prop={'size': 8})   # создаём легенду
    
    # добавляем график в объект QLabel
    canvas = FigureCanvasQTAgg(my_figure)
    layout = QVBoxLayout()
    layout.deleteLater()
    layout.addWidget(canvas)
    layout.addStretch(1)
    label.setLayout(layout)


# проверяет, все ли поля заполнены, и верно ли это логически
def check_boundaries(start_text, end_text):
    if len(start_text) == 0:
        create_error('Не введено начало отрезка', 'Ошибка границ')
        return False
    if len(end_text) == 0:
        create_error('Не введен конец отрезка', 'Ошибка границ')
        return False
    
    try:
        st_val = float(start_text)
        en_val = float(end_text)
        
        if st_val >= en_val:
            create_error('Границы отрезка (a >= b)', 'Ошибка границ')
            return False
        return True
    
    except ValueError:
        create_error('Перевод данных', 'Ошибка границ')
        return False


# делает элементарную проверку на верность введённое функции
def check_func_primary(func):
    my_func = str(func)
    func_sym = 'x0123456789+-*^/().'
    func_trig = ['log', 'sin', 'cos', 'exp', 'tan', 'e', 'sqrt', 'abs']

    if len(my_func) == 0:
        create_error('Не введена функция', 'Ошибка функции')
        return False
    
    for element in func_trig:
        my_func = my_func.replace(f"{element}", '')
    for element in func_sym:
        my_func = my_func.replace(f"{element}", '')

    if len(my_func) > 0:
        create_error('Функция неправильна', 'Ошибка функции')
        return False
    
    return True


# делает проверку на то, что погрешность измерения хотя бы меньше 1%, чем длина отрезка
def check_eps(st_val, en_val, eps_text):
    if len(eps_text) == 0:
        create_error('Не введена погрешность', 'Ошибка погрешности')
        return False
    try:
        eps_val = float(eps_text)

        if (en_val - st_val) / 100 <= eps_val:
            create_error('Погрешность >= 1% от отрезка', 'Ошибка погрешности')
            return False
        return True, ''
    except ValueError:
        create_error('Перевод погрешности', 'Ошибка погрешности')
        return False


# проверка, введено ли максимальное кол-во итераций для вычисления корней
def check_iters_cnt(max_cnt_text):
    if len(max_cnt_text) == 0:
        create_error('Не введено максимальное \nкол-во итераций', 'Ошибка итераций')
        return False
    try:
        mx_iters_val = int(max_cnt_text)

        if mx_iters_val < 3:
            create_error('Сомнительное кол-во операций', 'Ошибка итераций')
            return False
    except ValueError:
        create_error('Перевод максимального \nкол-во итераций', 'Ошибка итераций')
        return False
    return True, ''


# проверка, корректно ли введён шаг разбиения
def check_step(st_val, en_val, step_text):
    if len(step_text) == 0:
        create_error('Не введён шаг разбиения', 'Ошибка шага')
        return False
    
    try:
        step_val = float(step_text)
        
        if (en_val - st_val) < step_val:
            create_error('Шаг разбиения больше\nотрезка', 'Ошибка шага')
            return False
        elif step_val <= 0:
            create_error('Шаг разбиения (<=0)', 'Ошибка шага')
            return False

    except ValueError:
        create_error('Перевод шага разбиения', 'Ошибка шага')
        return False
    return True, ''


def check_continuous(start_val, end_val, func_text):
    func_text = func_text.replace("^", "**")
    rc, val = is_continuous(start_val, end_val, func_text)
    if not rc:
        create_error(f"Функция не может быть \nпосчитана в точке {val}", "Ошибка счёта")
        return False
    return True


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
    # для отчистки графика, на его месте делаем пустой график
    my_subplot = my_figure.add_subplot()
    my_subplot.plot([0], [0])
    my_subplot.grid()

    canvas = FigureCanvasQTAgg(my_figure)

    layout = QVBoxLayout()
    layout.deleteLater()
    layout.addWidget(canvas)
    layout.addStretch(1)

    label.setLayout(layout)


# разбиение на элементарные отрезки
def gen_array(start, end):
    step = (end - start) / 1000
    array = []
    cur_val = start
    while cur_val < end:
        array.append(cur_val)
        cur_val += step
    array.append(end)
    return array 


# разбиение на элементарные отрезки по шагу
def gen_array_with_step(start, end, step):
    array = []
    cur_val = start
    while cur_val < end:
        array.append(cur_val)
        cur_val += step
    array.append(end)
    return array


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
