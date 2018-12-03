class UFOCaseWeather:

    __slots__ = ["temperature",
                 "visibility",
                 "conditions"]

    def __init__(self,
                 temperature,
                 visibility,
                 fog,
                 hail,
                 rain,
                 snow,
                 thunder,
                 tornado):
        self.temperature = temperature
        self.visibility = visibility
        self.conditions = []

        # I figured this might be useful when displaying weather conditions
        # for example this means you could do something like:
        # "Weather Conditions: %s" % ", ".join(weather.conditions)
        # Instead of checking whether each of these is True.
        if fog is True:
            self.conditions.append("Fog")
        if hail is True:
            self.conditions.append("Hail")
        if rain is True:
            self.conditions.append("Rain")
        if snow is True:
            self.conditions.append("Snow")
        if thunder is True:
            self.conditions.append("Thunder")
        if tornado is True:
            self.conditions.append("Tornado")

    def __str__(self):
        format = '''Temperature: {0}C; Visibility: {1}km; Conditions: {2}'''
        if len(self.conditions) > 0:
            return format.format(self.temperature,
                                 self.visibility,
                                 ", ".join(self.conditions))
        else:
            return format.format(self.temperature,
                                 self.visibility,
                                 "None")
