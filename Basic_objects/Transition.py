import re


class Transition:
    def __init__(self, from_state, to_state, input_key, output_key):

        self.from_state = from_state
        self.to_state = to_state
        # self.input_symbol = input_symbol
        self.input_key = input_key
        # self.output_symbol = output_symbol
        self.output_key = output_key
        self.label = f'{self.input_key}/{self.output_key}'
        # self.set_input_output()


    def __repr__(self):
        return f'Transition({self.input_key}/{self.output_key})'

    def __eq__(self, other):
        if isinstance(other, Transition):
            return (self.input_key == other.input_key and self.output_key == other.output_key
                    and self.from_state == other.from_state and self.to_state == other.to_state)
        return False
    def __hash__(self):
        return hash((self.from_state, self.to_state, self.input_key, self.output_key))

    def set_input_output(self):
        # index = self.label.find(' / ')
        # if index != -1:
        #     self.input = self.label[:index]
        #     self.output = self.label[index + 3:]
        # input output are sperated by / with or without white space
        match = re.search(r'\s*/\s*', self.label)
        if match:
            input_end = match.start()
            output_start = match.end()
            self.input_key = self.label[:input_end]
            self.output_key = self.label[output_start:]

    def is_self_loop(self):
        return self.from_state == self.to_state

    def is_label_match(self, label):
        _input, _output = self.split_input_output(label)
        if _input and _output:
            return self.input_key == _input and self.output_key == _output
        return False

    def split_input_output(self, label):
        match = re.search(r'\s*/\s*', label)
        if match:
            input_end = match.start()
            output_start = match.end()
            _input = label[:input_end]
            _output = label[output_start:]
            return _input, _output
        return None, None