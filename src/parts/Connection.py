class Connection:

    def __init__(self, source, sink, strength):
        # connected BrainCells
        self.source = source
        self.sink = sink
        # connection
        self.strength = strength
