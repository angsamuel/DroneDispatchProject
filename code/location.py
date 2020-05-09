class Location():
    def __init__(self, locationType, idCode, x, y):
        self.locationType = locationType
        self.idCode = locationType + str(idCode)
        self.x = x
        self.y = y