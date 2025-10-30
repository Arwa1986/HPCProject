import re

from Basic_objects.Graph import Graph
from Basic_objects.State import State


class Tree:
    figure_num = 1
    input_counter = 0
    output_counter = 0

    def __init__(self):
        self.G = Graph()
        self.current_state_id = 0
        self.input_map = {}
        self.output_map = {}

    def add_input_to_map(self, input_label):
        if input_label not in self.input_map:
            self.input_map[input_label] = f'{Tree.input_counter}'
            Tree.input_counter += 1
        return f'{self.input_map[input_label]}'

    def add_output_to_map(self, output_label):
        if output_label not in self.output_map:
            self.output_map[output_label] = f'{Tree.output_counter}'
            Tree.output_counter += 1
        return f'{self.output_map[output_label]}'

    # def add_pos_trace(self, trace):
    #     input_alphabet_set = set()
    #     output_alphabet_set = set()
    #     alphabet = set()
    #     # if the graph is empty add the first trace
    #     if self.G.is_empty() :
    #         current_state = State(self.current_state_id, type = "accepted")
    #         self.G.add_state(current_state)
    #         self.G.set_initial_state(current_state)
    #
    #         for i in range(len(trace)):
    #             #  add transaction
    #             self.current_state_id += 1
    #             to_state = State(self.current_state_id, type = "accepted")
    #             self.G.add_state(to_state)
    #             input_key, output_key = self.split_input_output(trace[i])
    #             # input_key = self.add_input_to_map(input_label)
    #             # output_key = self.add_output_to_map(output_label)
    #             new_transition = self.G.add_transition(current_state, to_state, input_key, output_key)
    #             # input_alphabet_set.add(new_transition.input)
    #             # output_alphabet_set.add(new_transition.output)
    #             alphabet.add(f'{new_transition.input_key}/{new_transition.output_key}')
    #             # the distination now become the source for the next transaction
    #             current_state = to_state
    #     else:
    #         current_state = self.G.initial_state
    #         current_index = 0
    #         i=0
    #         while i  < len(trace):
    #             input_label, output_label = self.split_input_output(trace[i])
    #             input_key = self.input_map[input_label] if input_label in self.input_map else self.add_input_to_map(input_label)
    #             output_key = self.output_map[output_label] if output_label in self.output_map else self.add_output_to_map(output_label)
    #             if self.G.has_outgoing_transition_for_label(current_state, input_key, output_key):
    #                 current_state = self.G.get_target_state_for_label(current_state, input_key, output_key)
    #             else:
    #                 current_index = i
    #                 break
    #             i+=1
    #         if current_index < len(trace) and i<len(trace):
    #             for j in range(current_index, len(trace)):
    #                 #  add transaction
    #                 self.current_state_id += 1
    #                 to_state = State(self.current_state_id, type = "accepted")
    #                 self.G.add_state(to_state)
    #                 input_key, output_key = self.split_input_output(trace[j])
    #                 # input_key = self.add_input_to_map(input_label)
    #                 # output_key = self.add_output_to_map(output_label)
    #                 new_transition = self.G.add_transition(current_state, to_state, input_key, output_key)
    #                 # input_alphabet_set.add(new_transition.input)
    #                 # output_alphabet_set.add(new_transition.output)
    #                 alphabet.add(f'{new_transition.input_key}/{new_transition.output_key}')
    #                 # the distination now become the source for the next transaction
    #                 current_state = to_state
    #     return input_alphabet_set, output_alphabet_set, alphabet
    #
    # def add_neg_trace(self, trace):
    #     input_alphabet_set = set()
    #     output_alphabet_set = set()
    #     alphabet = set()
    #     # if the graph is empty add the first trace
    #     if self.G.is_empty() :
    #         current_state = State(self.current_state_id, type = "accepted")
    #         self.G.add_state(current_state)
    #         self.G.set_initial_state(current_state)
    #
    #         for i in range(len(trace)):
    #             #  add transaction
    #             self.current_state_id += 1
    #
    #             if i == len(trace) - 1:
    #                 to_state = State(self.current_state_id, type = "rejected")
    #             else:
    #                 to_state = State(self.current_state_id, type = "accepted")
    #             self.G.add_state(to_state)
    #             input_key, output_key = self.split_input_output(trace[i])
    #             # input_key = self.add_input_to_map(input_label)
    #             # output_key = self.add_output_to_map(output_label)
    #             new_transition = self.G.add_transition(current_state, to_state, input_key, output_key)
    #             # input_alphabet_set.add(new_transition.input)
    #             # output_alphabet_set.add(new_transition.output)
    #             alphabet.add(f'{new_transition.input_key}/{new_transition.output_key}')
    #             # the distination now become the source for the next transaction
    #             current_state = to_state
    #     else:
    #         current_state = self.G.initial_state
    #         current_index = 0
    #         i=0
    #         while i  < len(trace):
    #             input_label, output_label = self.split_input_output(trace[i])
    #             input_key = self.input_map[input_label] if input_label in self.input_map else self.add_input_to_map(
    #                 input_label)
    #             output_key = self.output_map[
    #                 output_label] if output_label in self.output_map else self.add_output_to_map(output_label)
    #             if self.G.has_outgoing_transition_for_label(current_state, input_key, output_key):
    #                 current_state = self.G.get_target_state_for_label(current_state, input_key, output_key)
    #             else:
    #                 current_index = i
    #                 break
    #             i+=1
    #         if current_index < len(trace) and i<len(trace):
    #             for j in range(current_index, len(trace)):
    #                 #  add transaction
    #                 self.current_state_id += 1
    #                 if j == len(trace) - 1:
    #                     to_state = State(self.current_state_id, type="rejected")
    #                 else:
    #                     to_state = State(self.current_state_id, type="accepted")
    #                 self.G.add_state(to_state)
    #                 input_key, output_key = self.split_input_output(trace[j])
    #                 # input_key = self.add_input_to_map(input_label)
    #                 # output_key = self.add_output_to_map(output_label)
    #                 new_transition = self.G.add_transition(current_state, to_state, input_key, output_key)
    #                 # input_alphabet_set.add(new_transition.input)
    #                 # output_alphabet_set.add(new_transition.output)
    #                 alphabet.add(f'{new_transition.input_key}/{new_transition.output_key}')
    #                 # the distination now become the source for the next transaction
    #                 current_state = to_state
    #     return input_alphabet_set, output_alphabet_set, alphabet

    # def build_tree(self, positive_traces, negative_traces= None):
    #     if negative_traces is None:
    #         negative_traces = []
    #     all_input = set()
    #     all_output = set()
    #     alphabet_set = set()
    #     for t in positive_traces:
    #         input_set, output_set, alphabet = self.add_pos_trace(t)
    #         for i in input_set:
    #             all_input.add(i)
    #         for o in output_set:
    #             all_output.add(o)
    #         for a in alphabet:
    #             alphabet_set.add(a)
    #     for t in negative_traces:
    #         input_set, output_set, alphabet = self.add_neg_trace(t)
    #         for i in input_set:
    #             all_input.add(i)
    #         for o in output_set:
    #             all_output.add(o)
    #         for a in alphabet:
    #             alphabet_set.add(a)
    #     self.G.set_alphabet(list(alphabet_set))
    #     self.G.set_input_alphabet(list(all_input))
    #     self.G.set_output_alphabet(list(all_output))
    #     return list(all_input), list(all_output), list(alphabet_set)

    def add_pos_trace_for_labeled_tree(self, RefDFA_G, trace):
        # input_alphabet_set = set()
        # output_alphabet_set = set()
        alphabet_set = set()
        currentStateRefDFA = RefDFA_G.initial_state
        # if the graph is empty add the first trace
        if self.G.is_empty() :
            current_state = State(self.current_state_id, type="accepted")
            current_state.set_reference_state(currentStateRefDFA)
            self.G.add_state(current_state)
            self.G.set_initial_state(current_state)

            for i in range(len(trace)):
                # add new state to the PTA + label it with the next state of the reference DFA
                input_key, output_key = self.split_input_output(trace[i])
                RefDFA_to_state = RefDFA_G.get_target_state_for_label(currentStateRefDFA, input_key, output_key)
                self.current_state_id += 1
                to_state = State(self.current_state_id, type="accepted")
                to_state.set_reference_state(RefDFA_to_state)
                self.G.add_state(to_state)
                #  add transaction
                new_transition = self.G.add_transition(current_state, to_state, input_key, output_key)
                alphabet_set.add(f'{new_transition.input_key}/{new_transition.output_key}')
                # the distination now become the source for the next transaction
                current_state = to_state
                currentStateRefDFA = RefDFA_to_state
        else:
            current_state = self.G.initial_state
            current_index = 0
            i=0
            while i  < len(trace):
                input_key, output_key = self.split_input_output(trace[i])
                if self.G.has_outgoing_transition_for_label(current_state, input_key, output_key):
                    current_state = self.G.get_target_state_for_label(current_state, input_key, output_key)
                    currentStateRefDFA = RefDFA_G.get_target_state_for_label(currentStateRefDFA, input_key, output_key)
                else:
                    current_index = i
                    break
                i+=1
            if current_index < len(trace) and i<len(trace):
                for j in range(current_index, len(trace)):
                    # add new state to the PTA + label it with the next state of the reference DFA
                    input_key, output_key = self.split_input_output(trace[j])
                    RefDFA_to_state = RefDFA_G.get_target_state_for_label(currentStateRefDFA, input_key, output_key)
                    self.current_state_id += 1
                    to_state = State(self.current_state_id, type="accepted")
                    to_state.set_reference_state(RefDFA_to_state)
                    self.G.add_state(to_state)
                    #  add transaction
                    new_transition = self.G.add_transition(current_state, to_state, input_key, output_key)
                    alphabet_set.add(f'{new_transition.input_key}/{new_transition.output_key}')
                    # the distination now become the source for the next transaction
                    current_state = to_state
                    currentStateRefDFA = RefDFA_to_state

        return alphabet_set

    def add_neg_trace_for_labeled_tree(self, RefDFA_G, trace):
        # input_alphabet_set = set()
        # output_alphabet_set = set()
        alphabet_set = set()
        currentStateRefDFA = RefDFA_G.initial_state
        # if the graph is empty add the first trace
        if self.G.is_empty() :
            current_state = State(self.current_state_id, type="accepted")
            current_state.set_reference_state(currentStateRefDFA)
            self.G.add_state(current_state)
            self.G.set_initial_state(current_state)

            for i in range(len(trace)):
                # add new state to the PTA + label it with the next state of the reference DFA
                input_key, output_key = self.split_input_output(trace[i])
                RefDFA_to_state = RefDFA_G.get_target_state_for_label(currentStateRefDFA, input_key, output_key)
                self.current_state_id += 1
                if i == len(trace) - 1:
                    to_state = State(self.current_state_id, type="rejected")
                else:
                    to_state = State(self.current_state_id, type="accepted")
                to_state.set_reference_state(RefDFA_to_state)
                self.G.add_state(to_state)
                #  add transaction
                new_transition = self.G.add_transition(current_state, to_state, input_key, output_key)
                alphabet_set.add(f'{new_transition.input_key}/{new_transition.output_key}')
                # the distination now become the source for the next transaction
                current_state = to_state
                currentStateRefDFA = RefDFA_to_state
        else:
            current_state = self.G.initial_state
            current_index = 0
            i=0
            while i  < len(trace):
                input_key, output_key = self.split_input_output(trace[i])
                if self.G.has_outgoing_transition_for_label(current_state, input_key, output_key):
                    current_state = self.G.get_target_state_for_label(current_state, input_key, output_key)
                    currentStateRefDFA = RefDFA_G.get_target_state_for_label(currentStateRefDFA,  input_key, output_key)
                else:
                    current_index = i
                    break
                i+=1
            if current_index < len(trace) and i<len(trace):
                for j in range(current_index, len(trace)):
                    # add new state to the PTA + label it with the next state of the reference DFA
                    input_key, output_key = self.split_input_output(trace[j])
                    RefDFA_to_state = RefDFA_G.get_target_state_for_label(currentStateRefDFA, input_key, output_key)
                    self.current_state_id += 1
                    if j == len(trace) - 1:
                        to_state = State(self.current_state_id, type="rejected")
                    else:
                        to_state = State(self.current_state_id, type="accepted")
                    to_state.set_reference_state(RefDFA_to_state)
                    self.G.add_state(to_state)
                    #  add transaction
                    new_transition = self.G.add_transition(current_state, to_state, input_key, output_key)
                    alphabet_set.add(f'{new_transition.input_key}/{new_transition.output_key}')
                    # the distination now become the source for the next transaction
                    current_state = to_state
                    currentStateRefDFA = RefDFA_to_state

        return alphabet_set

    def build_labeled_tree(self, RefDFA, positive_traces, negative_traces=None):
        self.input_map = RefDFA.input_map
        self.output_map = RefDFA.output_map
        if negative_traces is None:
            negative_traces = []
        # all_input = set()
        # all_output = set()
        alphabet_set = set()
        for t in positive_traces:
            alphabet = self.add_pos_trace_for_labeled_tree(RefDFA, t)
            for a in alphabet:
                alphabet_set.add(a)
        for t in negative_traces:
            alphabet = self.add_neg_trace_for_labeled_tree(RefDFA, t)
            for a in alphabet:
                alphabet_set.add(a)
        # for key, value in self.input_map.items():
        #     all_input.add(value)
        # for key, value in self.output_map.items():
        #     all_output.add(value)
        self.G.set_alphabet(list(alphabet_set))
        self.G.set_input_alphabet(RefDFA.input_alphabet)
        self.G.set_output_alphabet(RefDFA.output_alphabet)
        return list(alphabet_set)

    def split_input_output(self, label):
        match = re.search(r'\s*/\s*', label)
        _input = None
        _output = None
        if match:
            input_end = match.start()
            output_start = match.end()
            _input = label[:input_end]
            _output = label[output_start:]
        return _input, _output


# if __name__ == "__main__":
#     pta = Tree()
#     pta.add_pos_trace(['a/1', 'a/2', 'b/1', 'b/1'])
#     pta.add_neg_trace(['a/1', 'a/1', 'b/1'])
#     pta.add_neg_trace(['a/1', 'a/1', 'b/2'])
#     pta.G.print_graph()