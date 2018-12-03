from time import sleep, time

import requests

from .. import UFOCase
from .ufofeedpagesizeexception import InvalidPageSizeException


class UFOFeed:

    url_format = ("http://ufostalker.com:8080/mostRecentEvents"
                  "?page={0}&size={1}")

    __slots__ = ["count",
                 "max_sleep",
                 "stop_after",
                 "skip_existing",
                 "suppress_failed_requests",
                 "_last_sleep"]

    def __init__(self,
                 count=50,
                 max_sleep=300,
                 stop_after=None,
                 skip_existing=False,
                 suppress_failed_requests=False):
        '''This class is a generator for the UFOFeed, it is meant for monitoring
           the UFO Cases by iterating over them as they come in.
           For example, to print the next 5 new cases to console:
           for case in UFOFeed(stop_after=5, skip_existing=False):
               print(str(case))

        Keyword Arguments:
            count {int} -- Items per page. (default: {50}, min: {1}, max:{50})
            max_sleep {int} -- Max time between feed checks, (default: {300})
            stop_after {[type]} -- Stop after x UFO cases, (default: {None})
            skip_existing {bool} -- Do not iterate over the existing posts on
                                    the first page, only listen to new cases as
                                    they come in. (default: {False})
            suppress_failed_requests {bool} -- Attempt to suppress exceptions
                                               raised by failed HTTP requests
                                               to the UFO Stalker API. The site
                                               can fail to respond or the
                                               socket can time out or whatever
                                               this might maybe possibly help
                                               with that. (default: {False})
        '''

        if count > 50 or count < 1:
            raise InvalidPageSizeException("Count should be between 1 and 50.")
        self.count = count
        self.max_sleep = max_sleep
        self.stop_after = stop_after
        self.skip_existing = skip_existing
        self.suppress_failed_requests = suppress_failed_requests
        self._last_sleep = 0

    def __iter__(self):

        last_seen_id = 0
        seen = 0

        # Yield existing cases.
        if self.skip_existing:
            cases = self.get_recent_cases()
            last_seen_id = max([int(case.id) for case in cases])
            sleep(self.sleep_time)

        # Wait and yield new cases.
        while True:
            print("Check: " + str(time()))
            cases = reversed(self.get_recent_cases())
            new_cases = [c for c in cases if int(c.id > last_seen_id)]
            if len(new_cases) >= 1:
                for case in new_cases:
                    if self.stop_after is not None and seen >= self.stop_after:
                        return
                    yield case, seen
                    seen += 1
                self.reset_sleep_time()
                last_seen_id = max([int(c.id) for c in new_cases])
            sleep(self.sleep_time)

    @property
    def sleep_time(self):
        '''Returns a sleep time, this counts exponentially upwards to self.max_sleep.

        Returns:
            number -- Returns sleep time in seconds.
        '''
        if self._last_sleep < 1:
            self._last_sleep = 1
        elif self._last_sleep == 1:
            self._last_sleep = 2
        else:
            self._last_sleep = min(self._last_sleep ** 2, self.max_sleep)
            return self._last_sleep
        return min(self._last_sleep, self.max_sleep)

    def reset_sleep_time(self):
        '''Resets sleep time by resetting _last_sleep to 0.'''
        self._last_sleep = 0

    def get_recent_cases(self):
        '''Returns a list of up to self.count recent UFOCases.

        Raises:
            e -- If !self.suppress_failed_requests, raises e on request fail.

        Returns:
            List<UFOCase> -- Returns a list of UFOCase classes.
        '''
        r = None
        try:
            requests.get(self.url_format.format(0, self.count))
            r.raise_for_status()
        except Exception as e:
            if self.suppress_failed_requests:
                return []
            else:
                print("here")
                raise e
        else:
            cases = r.json()["content"]
            return [UFOCase(case["id"], case) for case in cases]
