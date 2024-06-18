class Connection:
    def __init__(self, neighbour: any, linkedColor=-1):
        self.neighbour = neighbour
        self.linkedColor = linkedColor
    
    def __repr__(self):
        return f"neighbour={self.neighbour.id}, linkedColor={self.linkedColor}\n"

    def __str__(self):
        return f"neighbour={self.neighbour.id}, linkedColor={self.linkedColor}\n"