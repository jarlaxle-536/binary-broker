from binary_broker.applications.trading.models import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



def get_data_on_commodities(timedelta):
    commodities = Commodity.objects.all()
    data = {
        cmd.name: cmd.get_last_records(timedelta)
        for cmd in commodities
    }
    return data

def run():
    data = get_data_on_commodities(CHOSEN_TIMEDELTA)
    print(data)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    for k, v in data.items():
        bla = [(k, float(v)) for k, v in v]
        plt.plot(*zip(*bla))
        plt.gcf().autofmt_xdate()
    plt.legend(list(data.keys()))
    plt.show()

CHOSEN_TIMEDELTA = datetime.timedelta(hours=4)
