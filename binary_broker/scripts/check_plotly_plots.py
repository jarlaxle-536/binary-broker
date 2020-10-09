from binary_broker.applications.trading.models import *
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from plotly.graph_objs import Scatter
from plotly.offline import plot
import random
import os

def get_data_on_commodities(timedelta):
    commodities = Commodity.objects.all()
    data = {
        cmd.name: cmd.get_last_records(timedelta)
        for cmd in commodities
    }
    return data

def run():
    data = get_data_on_commodities(CHOSEN_TIMEDELTA)
    price_history = list(data.values())[0]
    pl = plot(
        [Scatter(
            x=list(range(len(price_history))),
            y=[i[1] for i in price_history],
            mode='lines',
            name='test',
            opacity=0.8,
            marker_color='green')],
        output_type='div',
        displaylogo=False,
        include_plotlyjs=False)
    print(pl)
    print(data)

CHOSEN_TIMEDELTA = datetime.timedelta(minutes=1)
