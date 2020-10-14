import datetime

def get_time_dict():
    current_time = datetime.datetime.utcnow()
    time_string = current_time.strftime("%I:%M%p")
    dct = {'time_string': time_string}
    return dct
