def merge_dict(a, b):  #initial value of a is set to {}, b will get every item of dict as tuple
    key, value = b
    a[value] = a.get(value, []) + [key]
    return a
