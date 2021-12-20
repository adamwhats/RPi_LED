import math


def hex2rgb(h):
    return tuple(int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(r):
    return "#" + "".join(tuple('{:02X}'.format(i) for i in r))


def speed_map(i):
    """Exponential decay"""
    max_val = 500
    min_val = 1
    num_steps = 100
    k = math.log(min_val/max_val)/num_steps
    return int(max_val * math.exp(i * k))

def width_map(i):
    """linear map"""
    max_val = 2
    min_val = 0.1
    num_steps = 100
    return round(max_val - (i/num_steps) * (max_val - min_val), 2)


if __name__ == "__main__":
    pass
