import math

builtins = math.__dict__
EPS = 1e-8

# создание списка с результатами функции для аргументов
def function_output(x, this_function):
    y = []
    for x_val in x:
        val = eval(compile(this_function, "<string>", 'eval'), builtins, {"x": x_val})
        y.append(val)
    return y
    

# проверка, определена на функция во всех её точках
def is_continuous(a, b, func):
    step = 0.01
    for x in range(int(a * 1000), int(b * 1000), int(step * 100)):
        try:
            rc1, f1 = cnt_func(x/1000, func)
            rc2, f2 = cnt_func((x + step)/1000, func)
        
            if rc1 and rc2:
                if abs(f1 - f2) > 100:
                    return False, x/1000
            else:
                return False, x/1000
        except:
            return False, x/1000
    return True, ''


# упрощённый метод Ньютона для нахождения корня
def simple_newton_for_bound(my_function, a , b, eps, mx_cnt):
    x0 = (a + b) / 2
    i = 0
    while i < mx_cnt:
        i += 1
        rc1, fx0 = cnt_func(x0, my_function)
        f_prime_x0 = f_prime(x0, my_function)

        if not (rc1):
            break
        if f_prime_x0 == 0:
            return 2, x1, '-'
        
        x1 = x0 - fx0 / f_prime_x0

        if abs(x1 - x0) < eps:
            if abs(x1 - a) < EPS:
                return 3, x1, str(i)
            else:
                return 0, x1, str(i)
        
        x0 = x1
    return 1, '0', '-'


# функция, которая возвращает два массива (координаты x, y) для локальных экстремумов функции на отрезке
def get_locals_extremes(start_val, end_val, my_function):
    x_ar_extremes = []
    y_ar_extremes = []

    step = (end_val - start_val) / 1000
    cur_val = start_val
    f_x_prev = func_x(cur_val, my_function)
    cur_val += step
    f_x_cur = func_x(cur_val, my_function)

    while cur_val < end_val + step:
        f_x_next = func_x(cur_val + step, my_function)

        if (f_x_prev <= f_x_cur >= f_x_next) or (f_x_prev >= f_x_cur <= f_x_next):
            x_ar_extremes.append(cur_val)
            y_ar_extremes.append(f_x_cur)
        
        f_x_prev = f_x_cur
        f_x_cur = f_x_next
        cur_val += step

    return x_ar_extremes, y_ar_extremes


# функция, которая возвращает массив с координатой x, в которой функция принимает значение равное нулю
def get_roots(start_val, end_val, my_function):
    x_ar_roots = []

    step = (end_val - start_val) / 1000
    prev_val = start_val
    cur_val = start_val + step

    my_function = my_function.replace("^", "**")

    while cur_val < end_val:
        if is_root(prev_val, cur_val, my_function):
            x_ar_roots.append(cur_val - step * 0.5)

        prev_val = cur_val
        cur_val += step
    return x_ar_roots


# пытается понять, есть ли корень на отрезке
def is_root(a, b, func):
    f1 = func_x(a, func)
    f2 = func_x(b, func)

    if f1 * f2 <= 0:
        return True
    return False


# функция в точке с проверкой
def cnt_func(x, this_function):
    try:
        val = eval(compile(this_function, "<string>", 'eval'), builtins, {"x": x})
        return True, val
    except:
        return False, '0'


# функция в точке без проверки
def func_x(x, this_function):
    return eval(compile(this_function, "<string>", 'eval'), builtins, {"x": x})
    

# производная в точке
def f_prime(x, my_function):
    h = 0.0001
    rc1, res1 = cnt_func(x + h, my_function)
    rc2, res2 = cnt_func(x, my_function)
    if rc1 and rc2:
        return (res1 - res2) / h
