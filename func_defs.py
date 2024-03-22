import math

builtins = math.__dict__


# разбиение на отрезка по шагу
def gen_array(start, end, step):
    array = []
    while start < end:
        array.append(start)
        start += step
    array.append(end)
    return array 


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
        rc1, fx0 = cnt_func(x0, my_function)
        f_prime_x0 = f_prime(x0, my_function)

        if not (rc1):
            break
        if f_prime_x0 == 0:
            return 2, x1
        
        x1 = x0 - fx0 / f_prime_x0

        if abs(x1 - x0) < eps:
            return 0, x1
        
        x0 = x1
    return 1, '0'


# пытается понять, есть ли корень на отрезке
def is_root(a, b):
    if a * b > 0:
        return False
    return True


# функция в точке
def cnt_func(x, this_function):
    try:
        val = eval(compile(this_function, "<string>", 'eval'), builtins, {"x": x})
        return True, val
    except:
        return False, '0'
    

# производная в точке
def f_prime(x, my_function):
    h = 0.0001
    rc1, res1 = cnt_func(x + h, my_function)
    rc2, res2 = cnt_func(x, my_function)
    if rc1 and rc2:
        return (res1 - res2) / h
