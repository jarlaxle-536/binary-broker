from matplotlib import pyplot, dates

def create_price_plot(price_history, title=''):
    """
        Returns pyplot figure.
    """
    print('Price history:')
    print(*price_history, sep='\n')

    figure = pyplot.Figure()
    price_plot = figure.add_subplot(111)
    price_plot.plot(
        *zip(*price_history),
        'k'
    )
    price_plot.set_title(title)
    figure.autofmt_xdate()
    return figure
