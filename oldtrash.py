# Давидовский Кирилл. Группа ИУ7-24Б
# из задания по ТЗ - перевод из 10-ой в 6-ую СС и обратно
# Программа создана для того, чтобы создать мини-приложение: калькулятор
# реализован ввод с клавиатуры точки, удаления символа и всех цифр
# панели сверху с возможностью: 1 - вывода информации, 2 - выхода из приложения
# 3 - удалением одного символа, 4 - очищения строки, 5 - перевод из 10 в 6 СС
# 6 - перевод из 6 в 10 СС


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from conv_func import *


def create_my_window():
    # Создаём основное окно
    window = QMainWindow()
    window.setWindowTitle("Калькулятор")
    window.setFixedSize(500, 530 + 70)

    # Создаём задний фон
    label = QLabel(window)
    label.setFixedSize(500, 530 + 80)
    label.setStyleSheet("QLabel { background-image: url(my_icon.png); }")
    #label.setStyleSheet("background-color: rgb(125, 125, 125)")

    return window, label


# для создания окно с информацией о разработчике
def make_messagebox():
    message_box = QMessageBox()
    message_box.setWindowTitle("Info")   # заголовок
    message_box.setIcon(QMessageBox.Icon.Information)   # иконка
    message_box.setStandardButtons(QMessageBox.StandardButton.Close)   # кнопка
    message_box.setText("Мини-калькулятор, сделал\nДавидовский Кирилл,\nгруппа ИУ7-24Б\nПеревод из 6-ой СС")
    message_box.setFont(QFont("Arial",20))
    message_box.setStyleSheet("background-color: rgb(125, 125, 125)")

    return message_box


# делаем сверху меню с интерфейсом
def make_menu():
    bar = window.menuBar()
    bar.setFont(QFont("Arial",20))

    # создаём несколько вкладок
    # приложение, удаление, конвертация
    window.Calc_app = bar.addMenu("Приложение")
    window.Del = bar.addMenu("Удаление")
    window.Convert = bar.addMenu("Перевод")

    window.Calc_app.setFont(QFont("Arial",20))
    window.Del.setFont(QFont("Arial",20))
    window.Convert.setFont(QFont("Arial",20))

    # создаём функционал для первой вкладки и присваиваем ей
    # создание окна - информации о пользователе
    about = QAction("Информация", window)
    about.triggered.connect(message_box.exec)
    # создание окна с выходом из программы
    my_exit = QAction("Выход", window)
    my_exit.setShortcut('Ctrl+Q')
    my_exit.triggered.connect(app.quit)

    window.Calc_app.addAction(about)
    window.Calc_app.addAction(my_exit)

    # создаём функционал для второй вкладки и присваиваем ей
    delete_all = QAction("Удалить всё", window)
    delete_all.triggered.connect(button_is_ful_del)
    delete_one = QAction("Удалить элемент", window)
    delete_one.triggered.connect(button_is_del)

    window.Del.addAction(delete_all)
    window.Del.addAction(delete_one)

    # создаём функционал для третье вкладки и присваиваем ей
    # конвертация в новую систему
    convert_10_to_6 = QAction("Перевод из 10 в 6 СС", window)
    convert_10_to_6.triggered.connect(button_is_conv_in)
    # конвертация обратно
    convert_6_to_10 = QAction("Перевод из 6 в 10 СС", window)
    convert_6_to_10.triggered.connect(button_is_conv_out)

    window.Convert.addAction(convert_10_to_6)
    window.Convert.addAction(convert_6_to_10)


# создаём окно ввода, устанавливаем параметры и пишем регулярное выражение для ограничения ввода
def make_textbox():
    textbox = QLineEdit(window)
    textbox.setFont(QFont("Arial",34))
    textbox.resize(400, 70)   # устанавливаем размер
    textbox.move(50, 20 + 75)   # позиция
    textbox.setMaxLength(15)   # максимальное кол-во символов
    # регулярка для проверки вводимых значений
    textbox.setValidator(QRegularExpressionValidator(QRegularExpression("^([1-9][0-9]*|0)(\\.)[0-9]{15}")))
    textbox.setStyleSheet("background-color: rgb(110, 117, 67); border-radius: 4px;")

    return textbox


# функция для создания клавиш по координатам, размеру и тексту
def make_button(txt, wind, x, y, width, height):
    button = QPushButton(txt, wind)   # создание через указание текста и куда помещать
    button.setEnabled(True)
    button.setFixedSize(width, height)   # фиксируем размер
    button.move(x, y + 70)   # ставим в позицию
    button.setStyleSheet("background-color: rgb(0, 89, 88);border: 1px solid black;border-radius: 6px;")
    button.setFont(QFont("Arial", 19))

    return button


def make_and_connect_buttons():
    # я тебе уже говорил, что такое безумие?...
    # создание клавиш
    button_1 = make_button('1', window, 50, 110, 85, 90)
    button_2 = make_button('2', window, 155, 110, 85, 90)
    button_3 = make_button('3', window, 260, 110, 85, 90)
    button_4 = make_button('4', window, 50, 210, 85, 90)
    button_5 = make_button('5', window, 155, 210, 85, 90)
    button_6 = make_button('6', window, 260, 210, 85, 90)
    button_7 = make_button('7', window, 50, 310, 85, 90)
    button_8 = make_button('8', window, 155, 310, 85, 90)
    button_9 = make_button('9', window, 260, 310, 85, 90)
    button_0 = make_button('0', window, 155, 410, 85, 90)

    button_in = make_button('10->6', window, 365, 310, 85, 90)
    button_out = make_button('6->10', window, 365, 410, 85, 90)

    button_dot = make_button('.', window, 260, 410, 85, 90)

    button_delete = make_button('AC', window, 365, 210, 85, 90)
    button_backspace = make_button('<-', window, 365, 110, 85, 90)

    # соединяем клавиши с функциями
    button_1.clicked.connect(button_is_num)
    button_2.clicked.connect(button_is_num)
    button_3.clicked.connect(button_is_num)
    button_4.clicked.connect(button_is_num)
    button_5.clicked.connect(button_is_num)
    button_6.clicked.connect(button_is_num)
    button_7.clicked.connect(button_is_num)
    button_8.clicked.connect(button_is_num)
    button_9.clicked.connect(button_is_num)
    button_0.clicked.connect(button_is_num)

    button_in.clicked.connect(button_is_conv_in)
    button_out.clicked.connect(button_is_conv_out)

    button_dot.clicked.connect(button_is_dot)

    button_delete.clicked.connect(button_is_ful_del)
    button_backspace.clicked.connect(button_is_del)


# если клавиша - цифра, то добавляем её в строку
def button_is_num():
    button = QApplication.instance().sender()
    textbox.setText(textbox.text() + button.text())


# для перевода числа из 10 в нашу шестеричную СС с проверкой на максимальную длину
def button_is_conv_in():
    cur_exp = textbox.text()
    my_sys = 6
    mx_len_of_str = 15   # максимальная длина строки

    # делаем конвертацию
    new_num = conv_in_sys(cur_exp, my_sys)
    if len(new_num) > mx_len_of_str:   # проверка на то, поместится ли выражение в предел символов
        error_proc("\n   Ошибка ввода\n   много символов", "Ошибка размера")
    else:
        textbox.setText(new_num)


# для перевода из нашей шестеричной СС в десятичный вид с проверкой на валидность данных
def button_is_conv_out():
    cur_exp = textbox.text()
    my_sys = 6

    # проверка, все ли символы могут находится в нашей СС
    if is_valid(cur_exp, my_sys):
        new_num = conv_from_sys(cur_exp, my_sys)
        textbox.setText(new_num)
    # иначе генерируем ошибку
    else:
        error_proc("   Ошибка значения.\n  Символы в строке\n  не входит в 6 СС", "Ошибка значения")


# если кнопка - точка 
def button_is_dot():
    cur_exp = textbox.text()

    # если точка нет, создаём её
    if not('.' in cur_exp):
        if len(textbox.text()) == 0:
            # создаём ноль до точки, чтобы было корректно
            text = '0.'
            textbox.setText(text)
        else:
            text = '.'
            textbox.setText(textbox.text() + text)
    # иначе создаём ошибку о наличии точки в строке
    else:
        # кидаем ошибку, если точка уже есть
        error_proc("      Ошибка точки,\n точка уже находится\n    в выражении", 'Ввод точки')


# если строка не пустая, удаляем последний элемент
def button_is_del():
    cur_text = textbox.text()
    if len(cur_text) != 0:
        if cur_text:
            textbox.setText(cur_text[:-1])


# очищает строку
def button_is_ful_del():
    textbox.setText('')


# Создание ошибки
def error_proc(txt_of_error, head):
    # создаём окно диалога
    dot_error = QDialog(window)
    dot_error.setWindowTitle(head)
    dot_error.setFixedSize(200, 100)
    dot_error.setFont(QFont("Arial", 18))
    dot_error.setStyleSheet("background-color: rgb(78, 87, 84);border-radius: 4px;")
    # создаём окно с текстом ошибки
    text_er = QLabel(dot_error)
    text_er.move(8, 5)
    text_er.setStyleSheet("background-color: rgb(78, 87, 84);border-radius: 4px;")
    text_er.setText(txt_of_error)
    text_er.setFont(QFont("Arial", 13))
    # создаём кнопку для закрытия окна
    button_exit = QPushButton("ОК", dot_error)
    button_exit.setStyleSheet("background-color: rgb(75, 0, 130);border-radius: 4px;")
    button_exit.setGeometry(QRect(70, 67, 60, 30))
    button_exit.clicked.connect(dot_error.done)
    # запуск ошибки
    dot_error.exec()


# создание мини картинки для атмосферы
def add_picture():
    picture = QLabel(window)
    pix_map = QPixmap('dead_IU7_inside.jpg').scaled(85, 90)
    picture.setPixmap(pix_map)
    picture.setGeometry(QRect(50, 410 + 70, 85, 90))


#main#
app = QApplication([])

window, label = create_my_window()   # Создаём фон 
message_box = make_messagebox()   # Создаём окошко с информацией о разработчике ЛБ
bar = make_menu()   # создаём меню
textbox = make_textbox()   # создаём окно, c вводом
make_and_connect_buttons()   # создаём клавиши и соединяем их с действиями
add_picture()   # добавляем картинку на +10% к сдаче лабы

window.show()

app.exec()
