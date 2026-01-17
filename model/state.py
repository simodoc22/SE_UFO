
class State:
    def __init__(self,id,name,lat,lng,neighbors):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.neighbors = neighbors

    def __str__(self):
        return f"{self.name}"

    def __hash__(self):
        return hash(self.id)
