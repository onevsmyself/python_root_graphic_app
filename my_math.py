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
        is_worked, val = func(x_val, function)
        if is_worked:
            y.append(val)
        else:
            return []
    return y
    

def func(x, function):
    try:
        val = eval(function)
        return True, val
    except:
        return False, '0'
    

# def root(function, max_cnt, eps):



