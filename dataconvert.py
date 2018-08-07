def float_location(data):
    d = float(data[0][0]) / float(data[0][1])
    m = float(data[1][0]) / float(data[1][1])
    s = float(data[2][0]) / float(data[2][1])

    return d + (m / 60.0) + (s / 3600.0)