from .ufocasecoordinates import UFOCaseCoordinates


class UFOCaseLocation:

    __slots__ = ["location_name",
                 "coordinates",
                 "country",
                 "region",
                 "county",
                 "city",
                 "zipcode"]

    def __init__(self,
                 location_name,
                 longitude,
                 latitude,
                 country,
                 region,
                 county,
                 city,
                 zipcode):
        self.location_name = location_name
        self.coordinates = UFOCaseCoordinates(longitude, latitude)
        self.country = country
        self.region = region
        self.county = county
        self.city = city
        self.zipcode = zipcode

    def __str__(self):
        return self.location_name
