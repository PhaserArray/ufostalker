class UFOCaseSpecifics:

    __slots__ = ["type",
                 "shape",
                 "altitude",
                 "distance",
                 "duration",
                 "features",
                 "flight_path",
                 "landing_occurred",
                 "entity_encountered"]

    def __init__(self,
                 type,
                 shape,
                 altitude,
                 distance,
                 duration,
                 features,
                 flight_path,
                 landing_occurred,
                 entity_encountered):
        self.type = type
        self.shape = shape
        self.altitude = altitude
        self.distance = distance
        self.duration = duration
        self.features = features
        self.flight_path = flight_path
        self.landing_occurred = landing_occurred
        self.entity_encountered = entity_encountered
