import math

builtins = math.__dict__

def gen_array(start, end, step):
    array = []
    while start < end:
        array.append(start)
        start += step
    array.append(end)
    return array 


def function_output(x, function):
    y = []
    for x_val in x:
        is_success, val = func(x_val, function)
        if is_success:
            y.append(val)
    return y
    

def func(x, function):
    try:
        val = eval(compile(function, "<string>", 'eval'), builtins, {"x": x})
        return True, val
    except:
        print(x, func)
        return False, '0'


# Упрощенный метод Ньютона, также известный как модифицированный метод Ньютона
# Основной принцип упрощенного метода Ньютона состоит в замене производной f'(x) в формуле обновления на некоторую фиксированную константу. То есть, на каждой итерации k вычисляется новое предполагаемое значение xk с использованием следующей формулы: xk = xk-1 - f(xk-1)/c, где с - фиксированная константа.
    
