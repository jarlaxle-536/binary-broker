from matplotlib import pyplot, dates

def create_mp_price_plot_figure(price_history, title=''):
    """
        Returns pyplot figure.
    """
#    print('Price history:')
#    print(*price_history, sep='\n')

    figure = pyplot.Figure()
    price_plot = figure.add_subplot(111)
    price_plot.plot(
        *zip(*price_history),
        'k'
    )
#    price_plot.axes.set_aspect('equal')
    price_plot.set_title(title)
    figure.autofmt_xdate()
    return figure
