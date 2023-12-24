class Warehouse:
    def __init__(self, lat, long, id, maxCap, fixedCost = 1000, shippingCost = []):
        self.id = id;
        self.lat = lat
        self.long = long
        self.u = maxCap
        self.f = fixedCost
        self.c = shippingCost
