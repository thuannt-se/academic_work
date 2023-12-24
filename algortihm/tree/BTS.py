import networkx as nx

class BSTNode:
    def __init__(self, lat, long, demand=None):
        self.lat = lat
        self.long = long
        self.demand = demand