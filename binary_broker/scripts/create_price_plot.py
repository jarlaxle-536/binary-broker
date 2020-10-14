from binary_broker.applications.trading.auxiliary import *
from binary_broker.applications.trading.models import *


def show_figure(fig):

    # create a dummy figure and use its
    # manager to display "fig"
    dummy = pyplot.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)

def run():
    print(f'Timedelta: {CHOSEN_TIMEDELTA}')
    commodity = Commodity.objects.get(pk=CHOSEN_COMMODITY_ID)
    print(f'Commodity: {commodity}')
    price_history = commodity.get_last_records(CHOSEN_TIMEDELTA)
    price_plot = create_price_plot(
        price_history,
        title=commodity.name
    )
    show_figure(price_plot)
    price_plot.show()

CHOSEN_COMMODITY_ID = 1
CHOSEN_TIMEDELTA = datetime.timedelta(minutes=10)
