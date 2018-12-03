from datetime import datetime, timedelta

import requests

from .ufocaseweather import UFOCaseWeather
from .ufocaselocation import UFOCaseLocation
from .ufocasespecifics import UFOCaseSpecifics
from .ufocaseexception import InvalidUFOCaseException
from .ufocasetools import datetime_from_utcmstimestamp


class UFOCase:

    url_format = "http://www.ufostalker.com/sighting/{0}"
    api_url_format = "http://ufostalker.com:8080/event?id={0}"

    __slots__ = ["_id", "_data"]

    def __init__(self, id, data=None):
        self._id = id

        # To avoid unnecessary requests while using the UFO feed.
        if data is None:
            self.get_case_data()
        else:
            self._data = data

    def __str__(self):
        return "Case #{0} in {1}".format(self.id, self.location)

    def get_case_data(self):
        '''Fetches case data from UFO stalker, this can also be used to update the
           case data, but I'm not sure if the submitter can edit it after
           submission so this function may not be useful for anything except
           getting the initial data.

        Raises:
            InvalidUFOCaseException -- Raises InvalidUFOCaseException if case
                                       cannot be fetched due to a 400, 404,
                                       or 500 response code. That likely means
                                       the case doesn't exist, has been
                                       deleted, or the ID format is invalid.
        '''
        r = requests.get(UFOCase.api_url_format.format(self.id),
                         headers={"Accept": "application/json"})
        if r.status_code in (400, 404, 500):
            raise InvalidUFOCaseException("Failed to get case #%s!" % self.id)
        else:
            r.raise_for_status()
            self._data = r.json()

    @property
    def id(self):
        '''Case ID as a string.

        Returns:
            string -- Normally an integer in string format.
        '''
        return self._id

    @id.setter
    def id(self, x):
        '''Set the case ID, case will be auto-updated to match the new ID.

        Arguments:
            x {string} -- Case ID as a string.
        '''
        self._id = x
        self.get_case_data()

    @property
    def log_number(self):
        '''Some kind of UFO Case internal identifier.

        Returns:
            string -- Case log number, format not guranteed.
        '''
        return self._data["logNumber"]

    @property
    def url(self):
        '''User friendly URL to the UFO stalker case.

        Returns:
            string -- User friendly case URL.
        '''
        return UFOCase.url_format.format(self.id)

    @property
    def api_url(self):
        '''API URL to the UFO stalker case. By default this returns XML, you can
           specify application/json to get it in JSON.

        Returns:
            string -- Case API URL.
        '''
        return UFOCase.api_url_format.format(self.id)

    @property
    def summary(self):
        '''Returns the case summary, written by the submitter.

        Returns:
            string -- Case summary as a string.
        '''
        return self._data["summary"]

    @property
    def description(self):
        '''Returns the case description, written by the submitter.

        Returns:
            string -- Case description as a string.
        '''
        return self._data["detailedDescription"]

    @property
    def tags(self):
        '''Returns a list of the case tags.

        Returns:
            List<string> -- List of case tags.
        '''
        return self._data["tags"]

    @property
    def attachement_urls(self):
        '''Returns a list of attachement URLs.

        Returns:
            List<string> -- List of attachement URLs.
        '''
        return self._data["urls"]

    @property
    def occurred(self):
        '''Returns a datetime of the time this event occurred in UTC.

        Returns:
            datetime -- When the case occurred.
        '''
        return datetime_from_utcmstimestamp(float(self._data["occurred"]))

    @property
    def submitted(self):
        '''Returns a datetime of when the case was submitted in UTC.

        Returns:
            datetime -- When the case was submitted.
        '''
        return datetime_from_utcmstimestamp(float(self._data["submitted"]))

    @property
    def timezone(self):
        '''Returns the name of the timezone this occured in.
           This is NOT the timezone the "submitted" and "created" are in.

        Returns:
            string -- Name of the timezone.
        '''
        return self._data["timeZone"]

    @property
    def specifics(self):
        '''Returns the specific observations as UFOCaseSpecifics. This class
           contains the following properties: type, shape, altitude, distance,
           duration, features, flight_part, landing_occurred,
           and entity_encountered. Some or all of these may be None depending
           on the case.

        Returns:
            UFOCaseSpecifics -- Wrapper around the UFO sighting specifics.
        '''
        duration_td = None
        if self._data["duration"] is not None and self._data["duration"] != "":
            duration_dt = datetime.strptime(self._data["duration"], "%H:%M:%S")
            duration_td = timedelta(hours=duration_dt.hour,
                                    minutes=duration_dt.minute,
                                    seconds=duration_dt.second)
        return UFOCaseSpecifics(self._data["type"],
                                self._data["shape"],
                                self._data["altitude"],
                                self._data["distance"],
                                duration_td,
                                self._data["features"],
                                self._data["flightPath"],
                                self._data["landingOccurred"],
                                self._data["entityEncountered"])

    @property
    def location(self):
        '''Returns the location as UFOCaseLocation. This class
           contains the following properties: location_name, coordinates,
           country, region, county, city, zipcode. Some or all of these may be
           None depending on the case.

        Returns:
            UFOCaseLocation -- Wrapper around the location details.
        '''
        return UFOCaseLocation(self._data["locationName"],
                               self._data["longitude"],
                               self._data["latitude"],
                               self._data["country"],
                               self._data["region"],
                               self._data["county"],
                               self._data["city"],
                               self._data["zipcode"])

    @property
    def weather(self):
        '''Returns the weather as UFOCaseWeather. This class
           contains the following properties: temperature, visibility,
           conditions. Some or all of these may be None depending on the case.

        Returns:
            UFOCaseWeather -- Wrapper around the weather details of that day.
                              Can return None.
        '''
        if self._data["weather"] is not None:
            weather = self._data["weather"]["history"]["dailySummary"][0]
            return UFOCaseWeather(weather["meantempm"],
                                  weather["meanvism"],
                                  weather["fog"],
                                  weather["hail"],
                                  weather["rain"],
                                  weather["snow"],
                                  weather["thunder"],
                                  weather["tornado"])
        return None
