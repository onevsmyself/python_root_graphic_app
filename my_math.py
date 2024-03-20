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
