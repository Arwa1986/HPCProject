class X:
    def __init__(self, state_label, color_id):
        self.state_label = state_label
        self.color_id = color_id
    def __eq__(self, other):
        if isinstance(other, X):
            return self.state_label == other.state_label and self.color_id == other.color_id
        return False
    def __hash__(self):
        return hash((self.state_label, self.color_id))
    def __repr__(self):
        return f'X({self.state_label}, {self.color_id})'

class Z:
    def __init__(self, color_id):
        self.color_id = color_id
    def __eq__(self, other):
        if isinstance(other, Z):
            return self.color_id == other.color_id
        return False
    def __hash__(self):
        return hash(self.color_id)
    def __repr__(self):
        return f'Z({self.color_id})'

# class Y:
#     def __init__(self, input, parent_color_id, child_color_id):
#         self.input = input
#         # self.output = output
#         self.parent_color_id = parent_color_id
#         self.child_color_id = child_color_id
#     def __eq__(self, other):
#         if isinstance(other, Y):
#             return self.input == other.input and self.parent_color_id == other.parent_color_id and self.child_color_id == other.child_color_id
#         return False
#     def __hash__(self):
#         return hash((self.input, self.parent_color_id, self.child_color_id))
#     def __repr__(self):
#         return f'Y({self.input}, {self.parent_color_id}, {self.child_color_id})'
#
# class W:
#     def __init__(self, input, parent_color_id, output):
#         self.color_id = parent_color_id
#         self.input = input
#         self.output = output
#     def __eq__(self, other):
#         if isinstance(other, W):
#             return self.color_id == other.color_id and self.input == other.input and self.output == other.output
#         return False
#     def __hash__(self):
#         return hash((self.color_id, self.input, self.output))
#     def __repr__(self):
#         return f'W( {self.input}, {self.color_id}, {self.output})'

class YW:
    def __init__(self, input, output, parent_color_id, child_color_id):
        self.input = input
        self.parent_color_id = parent_color_id
        self.child_color_id = child_color_id
        self.output = output
    def __eq__(self, other):
        if isinstance(other, YW):
            return (self.input == other.input and
                    self.output == other.output and
                    self.parent_color_id == other.parent_color_id and
                    self.child_color_id == other.child_color_id
                    )
        return False
    def __hash__(self):
        return hash((self.input, self.output, self.parent_color_id, self.child_color_id))
    def __repr__(self):
        return f'YW({self.input}, {self.output} , {self.parent_color_id}, {self.child_color_id})'