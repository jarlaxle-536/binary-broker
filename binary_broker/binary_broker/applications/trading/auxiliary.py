def get_plot_points_from_data(
    data,
    min_x=0,
    min_y=0,
    width=100,
    height=50
    ):
    length = len(data)
    data = [(k, float(v)) for k, v in data]
    real_min = min([v for k, v in data])
    real_max = max([v for k, v in data])
    diff = (lambda v: v if v else 1)(real_max - real_min)
    scaled_data = [[
        min_x + i * width / length,
        min_y + height * (real_max - data[i][1]) / diff]
        for i in range(length)]
    result = ' '.join([' '.join(map(str, el)) for el in scaled_data])
    return result
