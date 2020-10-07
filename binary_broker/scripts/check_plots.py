from binary_broker.applications.trading.models import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random
import os

def get_data_on_commodities(timedelta):
    commodities = Commodity.objects.all()
    data = {
        cmd.name: cmd.get_last_records(timedelta)
        for cmd in commodities
    }
    return data

def create_svg_graphics(data):
    print('will create svg')
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res.html')
    template = """
    <svg viewBox="{min_x} {min_y} {width} {height}" class="chart">
      <polyline
         fill="none"
         stroke="#0074d9"
         stroke-width="3"
         points="{plot_points}">
      </svg>
    """
    context = dict()
    real_min = min([v for k, v in data])
    real_max = max([v for k, v in data])
    context['min_x'] = 0
    context['width'] = 100
    context['min_y'] = 0
    context['height'] = 100
    data = data
    scaled_data = [[
        context['min_x'] + i * context['width'] / len(data),
        context['min_y'] + context['height'] * (real_max - data[i][1]) / (real_max - real_min)]
        for i in range(len(data))]
    context['plot_points'] = ' '.join([' '.join(map(str, el)) for el in scaled_data])
    print(context['plot_points'])
    if os.path.exists(target):
        os.remove(target)
    res = template.format(**context)
    with open(target, 'a') as file:
        file.write(res)

def get_plot_points_from_data(data, min_x, min_y, width, height):
    length = len(data)
    real_min = min([v for k, v in data])
    real_max = max([v for k, v in data])
    scaled_data = [[
        min_x + i * width / length,
        min_y + height * (real_max - data[i][1]) / (real_max - real_min)]
        for i in range(length)]
    result = ' '.join([' '.join(map(str, el)) for el in scaled_data])
    return result

def run():
    data = get_data_on_commodities(CHOSEN_TIMEDELTA)
#    data = dict(list(data.items())[0])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    for k, v in data.items():
        bla = [(k, float(v)) for k, v in v]
        plt.plot(*zip(*bla))
        plt.gcf().autofmt_xdate()
    plt.legend(list(data.keys()))
    plt.show()
    create_svg_graphics(list(data.values())[0])

CHOSEN_TIMEDELTA = datetime.timedelta(hours=4, minutes=20)
