class BrainCell:

    def __init__(self):
        self.value = 0
        self.sum_of_inputs = 0
        self.type = None
        self.connects_to = []
        self.connects_from = []
        self.marked = False

    def add_connects_to(self, connection):
        self.connects_to.append(connection)

    def add_connects_from(self, connection):
        self.connects_from.append(connection)

    def is_marked(self):
        return self.marked

    def set_mark(self):
        self.marked = True

    def reset_mark(self):
        self.marked = False
