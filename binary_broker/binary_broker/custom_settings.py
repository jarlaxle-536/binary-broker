import datetime

GLOBAL_UPDATE_PERIOD = datetime.timedelta(seconds=5)

DEFAULT_NUMERIC_SETTINGS = {
    'max_digits': 10,
    'decimal_places': 2
}

# TRADING.MODELS.ASSET

ASSET_MANDATORY_FIELDS = ('name')

# TRADING.MODELS.BET

BET_MANDATORY_FIELDS = (
    'duration', 'direction_up', 'venture', 'asset', 'owner',
)

BET_DIRECTIONS = [(True, 'up'), (False, 'down')]
BET_IS_REAL = [(True, 'yes'), (False, 'no')]
BET_DURATIONS = [
    (10, '10 seconds'),
    (30, '30 seconds'),
    (60, '1 minute'),
    (120, '2 minutes')
]
BET_VENTURES = [(v, f'{v} $')
    for v in [1, 2, 5, 10, 20, 50, 100]]
