class BrainCell:

    def __init__(self):
        self.value = 0
        self.type = None
        self.connects_to = []
        self.connects_from = []

    def add_connects_to(self, connection):
        self.connects_to.append(connection)

    def add_connects_from(self, connection):
        self.connects_from.append(connection)