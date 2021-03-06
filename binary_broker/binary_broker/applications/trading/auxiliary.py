from matplotlib import pyplot, dates
import datetime

def create_mp_price_plot_figure(price_history, profile, title=''):
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
    time_endpoints = (lambda l:
        (min(l), max(l)))([dt for dt, pr in price_history])
    bets_to_repr = [b for b in profile.bet_set.all() if any(map(
        lambda dt: time_endpoints[0] <= dt <= time_endpoints[1],
        [b.time_start, b.time_finish]))
    ]
    print('bets', profile.bet_set.all())
    print('bets to represent:', bets_to_repr)
    for b in bets_to_repr:
        bet_points = [(dt, b.price_when_created) for dt in
        [b.time_start + datetime.timedelta(seconds=x) for x in
            range((b.time_finish - b.time_start).seconds)]
        if time_endpoints[0] <= dt <= time_endpoints[1]]
        print(bet_points)
        price_plot.plot(
            *zip(*bet_points),
        )
#    price_plot.axes.set_aspect('equal')
    price_plot.set_title(title)
    figure.autofmt_xdate()
    return figure

def add_mp_bet_plots(figure, profile):
    """
        figure: matplotlib price plot for some asset
        profile: current user profile
    """
    # get all profile bets that have at least one of their time endpoints in
    # current time period
    pass

def sign(val):
    return 1 if val > 0 else 0 if val == 0 else -1
