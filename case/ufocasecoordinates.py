class UFOCaseCoordinates:

    __slots__ = ["longitude", "latitude"]

    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def __str__(self):
        return "{0}, {1}".format(self.longitude, self.latitude)
