import datetime

GLOBAL_UPDATE_PERIOD = datetime.timedelta(seconds=5)

DEFAULT_NUMERIC_SETTINGS = {
    'max_digits': 10,
    'decimal_places': 2
}

# ACCOUNTS.MODELS.PROFILE

PROFILE_ACCOUNT_TYPES = [
    (v, str(v)) for v in ('Demo', 'Real')
]
PROFILE_ACCOUNT_TYPE_RELATED_NAMES = {
    'Demo': 'demo_account',
    'Real': 'real_account'
}

# TRADING.MODELS.ASSET

ASSET_MANDATORY_FIELDS = ('name', )

# TRADING.MODELS.BET

BET_MANDATORY_FIELDS = (
    'duration', 'direction_up', 'venture', 'asset', 'owner'
)

BET_DIRECTIONS = [(True, 'up'), (False, 'down')]
BET_IS_REAL = [(True, 'yes'), (False, 'no')]
BET_DURATIONS = [
    (1, '1 second'),
    (10, '10 seconds'),
    (30, '30 seconds'),
    (60, '1 minute'),
    (120, '2 minutes')
]
BET_VENTURES = [(v, f'{v} $')
    for v in [0, 1, 2, 5, 10, 20, 50, 100, 10 ** 6]]
BET_SUCCESS = [
    (1, 'Won'),
    (0, 'Equal'),
    (-1, 'Lost')
]
