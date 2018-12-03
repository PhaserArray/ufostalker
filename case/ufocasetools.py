from datetime import datetime, timedelta


def datetime_from_utcmstimestamp(mstimestamp):
    '''A wrapper around the datetime.utcfromtimestamp(timestamp) function f
        or millisecond timestamps that also works with negative timestamps.

    Arguments:
        mstimestamp {float} -- UTC Timestamp in Milliseconds

    Returns:
        datetime -- datetime from mstimestamp
    '''

    timestamp = mstimestamp * 1e-3
    if timestamp < 0:
        return datetime(1970, 1, 1) + timedelta(seconds=timestamp)
    else:
        return datetime.utcfromtimestamp(timestamp)
