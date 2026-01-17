class Sighting:
    def __init__(self,id,s_datetime,city,state,country,shape,duration,latitude,longitude):
        self.id = id
        self.s_datetime = s_datetime
        self.city = city
        self.state = state
        self.country = country
        self.shape = shape
        self.duration = duration
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"{self.id}"

    def __hash__(self):
        return hash(self.id)

