class State:

    def __init__(self, label, type="unlabeled", isInitial=False):
            self.label = label
            self.type = type # accpeted, rejected, or unlabeled
            self.isInitial = isInitial
            self.color = "white"
            # color code:
            # white: unlabeled
            #  red : can't merged with another red
            #  blue: cna be merged with a red state
            #  yellow: sink state - marked as rejected
            self.ref_state = None

    def __hash__(self):
        return hash(self.label)

    def __repr__(self):
        return f'State({self.label})'

    def __eq__(self, other):
        if isinstance(other, State):
            return self.label == other.label
        return False

    def getIncomingTransitions(self):
        pass

    def getOutgoingTransitions(self):
        pass

    def set_reference_state(self, ref_state):
        self.ref_state = ref_state

    def get_reference_state(self):
        return self.ref_state

    def print_state(self):
        print(f"State: {self.label}, Type: {self.type}, Is Initial: {self.isInitial}, Color: {self.color}")