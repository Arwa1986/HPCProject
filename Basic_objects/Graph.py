# from gc import enable
#
# from numpy.ma.core import append
# from orca.object_properties import RELATION_DETAILS_FOR

from Basic_objects.State import State
from Basic_objects.Transition import Transition


class Graph:
    def __init__(self):
        self.graph = {}
        self.initial_state = ""
        self.input_alphabet =[]
        self.output_alphabet =[]
        self.input_map = {}
        self.input_counter = 0
        self.output_map = {}
        self.output_counter = 0
        self.alphabet = []

    def __eq__(self, other):
        equal = False
        if self.initial_state == other.initial_state:
            if self.compare_dicts_of_dicts(self.graph, other.graph):
                            equal = True
        return equal

    def to_string(self):
        graph_str = ''
        for state, transitions in self.graph.items():
            graph_str.join(f"{state}:\n")
            if transitions:
                for neighbor, transaction in transitions.items():
                    graph_str.join(f"  -> {neighbor} via {transaction}\n")
            else:
                graph_str.join("  No outgoing transitions\n")

            if state.isInitial:
                graph_str.join("initial state\n")
        graph_str.join('==================================================================\n')
        return graph_str
    def compare_dicts_of_dicts(self, graph1, graph2):
        if graph1.keys() != graph2.keys():
            return False

        for key in graph1:
            if isinstance(graph1[key], dict) and isinstance(graph2[key], dict):
                if not self.compare_dicts_of_dicts(graph1[key], graph2[key]):
                    return False
            elif isinstance(graph1[key], list) and isinstance(graph2[key], list):
                if sorted(graph1[key]) != sorted(graph2[key]):
                    return False
            else:
                if graph1[key] != graph2[key]:
                    return False

        return True

    def is_empty(self):
        if len(self.graph) == 0:
            return True
        else:
            return False

    def set_initial_state(self, new_state:State):
        has_initial = False
        for state, transitions in self.graph.items():
            if state.isInitial:
                has_initial = True
                self.initial_state = state
                if self.initial_state == new_state:
                    return
                print(f"The graph already has an initial state: {self.initial_state}")
                return
        if not has_initial:
            self.initial_state = new_state
            self.initial_state.isInitial = True
    def get_initial_state(self):
        return self.initial_state

    def set_input_alphabet(self, input_alphabet):
        self.input_alphabet = input_alphabet
    def get_input_alphabet(self):
        return self.input_alphabet
    def add_to_input_map(self, input_symbol):
        if input_symbol not in self.input_map:
            self.input_map[input_symbol] = f'{self.input_counter}'
            key = f'{self.input_counter}'
            self.input_counter += 1
        else:
            key = f'{self.input_map[input_symbol]}'
        return key

    def set_output_alphabet(self, output_alphabet):
        self.output_alphabet = output_alphabet
    def get_output_alphabet(self):
        return self.output_alphabet
    def add_to_output_map(self, output_symbol):
        if output_symbol not in self.output_map:
            self.output_map[output_symbol] = f'{self.output_counter}'
            key = f'{self.output_counter}'
            self.output_counter += 1
        else:
            key = f'{self.output_map[output_symbol]}'
        return key


    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def get_alphabet(self):
        return self.alphabet

    def add_state(self, state:State):
        if state not in self.graph:
            self.graph[state] = {}

    def delete_state(self, state):
        if state in self.graph:
            del self.graph[state]

    def get_all_states(self):
        return list(self.graph.keys())

    def get_red_states(self):
        red_states = []
        for state in self.graph:
            if state.color == 'red':
                red_states.append(state)
        return red_states

    def get_state_for_label(self, label):
        for state in self.get_all_states():
            if state.label == label:
                return state
        return None

    def get_outgoing_transitions_for_state_with_input(self, state:State, input):
        if state in self.graph:
            for neighbor, transitions in self.graph[state].items():
                for tran in transitions:
                    if tran.input_key == input:
                        return tran
        return None

    def get_outgoing_transitions_for_state(self, state:State):
        list_of_outgoing_transitions = []
        if state in self.graph:
            for tran_list in self.graph[state].values():
                for item in tran_list:
                    list_of_outgoing_transitions.append(item)

        return list_of_outgoing_transitions
    def get_outgoing_transitions_for_list_of_states(self, s1, set_to_merge):
        out_transitions=[]
        for s in set_to_merge:
            if s != s1:
                s_out_trans = self.get_outgoing_transitions_for_state(s)
                for out_trans in s_out_trans:
                   out_transitions.append(out_trans)
        return out_transitions

    # returns all transitions of the graph
    def get_all_transitions(self):
        all_transitions = []
        all_states = self.get_all_states()
        for state in all_states:
            outgoing_transitions = self.get_outgoing_transitions_for_state(state)
            for t in outgoing_transitions:
                all_transitions.append(t)
        return all_transitions

    # returns all transitions of the graph as a set defined by the input/output pair
    def get_transitions_labels_set(self):
        transitions_set = set()
        for transition in self.get_all_transitions():
            transitions_set.add(tuple([transition.input, transition.output]))
        return transitions_set

    # Function to get all transitions for a given label
    def get_transitions_for_label(self, label):
        transitions = []
        for state, transitions_dict in self.graph.items():
            for to_state, transaction_list in transitions_dict.items():
                for transaction in transaction_list:
                    if transaction.label == label:
                        transitions.append(transaction)
        return transitions

    # Function to get incoming transitions for a given state
    def get_incoming_transitions(self, target_state):
        incoming_transitions = []
        for state, transitions in self.graph.items():
            for neighbor, transaction_list in transitions.items():
                if neighbor == target_state:
                    for transaction in transaction_list:
                        incoming_transitions.append(transaction)
        return incoming_transitions

    def has_incoming_transition_label(self, state, transition):
        if state in self.graph:
            for t in self.get_incoming_transitions(state):
                if (t.input_key == transition.input_key
                        and t.output_key == transition.output_key
                        and t.from_state == transition.from_state):
                    return True
        return False

    def add_transition(self, from_state:State, to_state:State, inputKey, outputKey):
        if from_state not in self.graph:
            self.add_state(from_state)
        if to_state not in self.graph[from_state]:
            self.graph[from_state][to_state]=[]

        new_edge = Transition(from_state, to_state, inputKey, outputKey)
        self.graph[from_state][to_state].append(new_edge)
        return new_edge

    def delete_Transition(self, transition:Transition):
        self.graph[transition.from_state][transition.to_state].remove(transition)
        if len(self.graph[transition.from_state][transition.to_state])==0:
           del self.graph[transition.from_state][transition.to_state]

    def get_transitions_between_states(self, source, target):
        return self.graph[source][target]

    # lambdaFunction returns the output for a given state with a given input
    # current_state is an State object, input is string
    def get_output(self, current_state, input):
        output = ""
        for to_state, transitions in self.graph[current_state].items():
            for tran in transitions:
                if tran.input_key == input:
                    return tran.output_key

        return output

    # returns the target_state for a given state with a given input
    def get_target_state(self, current_state, input):
        target_state = None
        for to_state, transitions in self.graph[current_state].items():
            for tran in transitions:
                if tran.input_key == input:
                    target_state = to_state

        return target_state

    def has_outgoing_transition_for_label(self, state, input_label, output_label):
        found = False
        for states, transitions in self.graph[state].items():
            for tran in transitions:
                if tran.input_key == input_label and tran.output_key == output_label:
                    found =True
        return found

    # returns the target_state for a given state with a given input
    def get_target_state_for_label(self, current_state, inputLabel, outputLabel):
        for to_state, transitions in self.graph[current_state].items():
            for tran in transitions:
                if tran.input_key == inputLabel and tran.output_key == outputLabel: #.label == trnsitionLabel:
                    return to_state
        return None

    # Function to print the graph
    def get_children(self, state):
        # if self.graph[state] == {}:
        #     return None
        return list(self.graph[state].keys())
    def get_descendants(self, state):
        # Initialize a set to keep track of visited states and a list for the stack
        visited = set()
        stack = [state]
        descendants = set()

        while stack:
            current_state = stack.pop()
            if current_state not in visited:
                visited.add(current_state)
                if current_state in self.graph:
                    for neighbor in self.graph[current_state]:
                        if neighbor not in visited:
                            stack.append(neighbor)
                            descendants.add(neighbor)

        return list(descendants)

    # have_shared_outgoing_transition: Boolean
    # True: if both states have shard an outgoing transition with the same label
    # the next state doesn't matter
    # False: if both states have totally different outgoing transitions
    def have_shared_outgoing_transition(self, state1, state2):
        share_label = False
        shared_labels = []
        # Collect labels of outgoing transitions for state1
        state1_outgoing_transitions = self.get_outgoing_transitions_for_state(state1)
        state1_labels = set()
        for transition in state1_outgoing_transitions:
            state1_labels.add(transition.label)

        # Collect labels of outgoing transitions for state2
        state2_outgoing_transitions = self.get_outgoing_transitions_for_state(state2)
        state2_labels = set()
        for transition in state2_outgoing_transitions:
            state2_labels.add(transition.label)

        # Check if there is any common label
        common_labels = state1_labels.intersection(state2_labels)

        return list(common_labels)

    def get_leaves(self):
        leaves = []
        all_states = self.get_all_states()
        for state in all_states:
            if self.graph[state] == {}:
                leaves.append(state)
        return leaves

    def get_states_with_selflopp_only(self):
        states_with_selflopp_only=[]
        all_states = self.get_all_states()
        for state in all_states:
            if self.get_children(state) == [state]:
                states_with_selflopp_only.append(state)
        return states_with_selflopp_only

    def print_graph(self):
        for state, transitions in self.graph.items():
            print(f"{state}-Ref({state.ref_state}):")
            if transitions:
                for neighbor, transaction in transitions.items():
                    print(f"  -> {neighbor} via {transaction}")
            else:
                print("  No outgoing transitions")

            if state.isInitial:
                print("initial state")
        print('==================================================================')

    def to_nusmv(self, patterns):
        states = self.get_all_states()
        transitions =  self.get_outgoing_transitions_for_list_of_states(None, states)

        contents = 'MODULE main\nVAR\nstate:{'

        for s in range(len(states)):
            contents += f'{states[s].label}'
            if s < len(states) - 1:
                contents += ', '
        contents += f'}};\n'

        contents += f'IVAR\n'
        contents += f'input:{{'
        inputs = self.get_input_alphabet()
        for i in range(len(inputs)):
            contents += f'{inputs[i]}'
            if i < len(inputs) - 1:
                contents += ', '
        contents += f'}};\n'

        contents += f'output:{{'
        outputs = self.get_output_alphabet()
        for o in range(len(outputs)):
            contents += f'{outputs[o]}'
            if o < len(outputs) - 1:
                contents += ', '
        contents += f'}};\n'
        states_input_map = {}
        contents += f'ASSIGN\n'\
                    f'init(state):={self.initial_state.label};\n'\
                    'next(state):=case\n'
        for t in transitions:
            contents += f'state = {t.from_state.label} & input = {t.input} : {t.to_state.label};\n'
            # if t.to_state not in states_input_map:
            #     states_input_map[t.to_state] = [t]
            # else:
            #     states_input_map[t.from_state].append(t)
        contents += f'TRUE : state;\n'
        contents += f'esac;\n'

        # block any transitions to blue states
        states_input_map, is_graph_input_enabled = self.is_graph_input_enabled()
        if not is_graph_input_enabled:
            contents += f'TRANS\n'
            for state, not_enabled_input in states_input_map.items():
                for input in not_enabled_input:
                    contents += f'!(state = {state.label} & input = {input}) &\n'
            # replace the last & with ;
            contents = contents.rsplit('&', 1)
            contents = ';'.join(contents)

        # Defining the output for each state/input
        contents += f'TRANS\n'
        for i in range(len(transitions)):
            contents += (f'(state = {transitions[i].from_state.label} & input = {transitions[i].input} '
                         f'-> output = {transitions[i].output})')
            if i < len(transitions) - 1:
                contents += f' &\n'
            else:
                contents += f';\n'

        for p in patterns:
            contents += f'LTLSPEC {p};\n'

        return contents

    def is_graph_input_enabled(self):
        input_enabled = True
        states_input_map = {} # map of states to the inputs that are not enabled
        for s in self.get_all_states():
            s_trans = self.get_outgoing_transitions_for_state(s)
            if len(s_trans) != len(self.get_input_alphabet()):
                input_enabled =  False
                enabled_input = [] # list of enabled inputs: inputs that have transitions from the state
                for t in s_trans:
                    enabled_input.append(t.input)
                for i in self.get_input_alphabet():
                    if i not in enabled_input:
                        if s not in states_input_map:
                            states_input_map[s] = [i]
                        else:
                            states_input_map[s].append(i)
        return states_input_map, input_enabled

    def is_disconnected(self):
        disconnected = False
        for s in self.get_all_states():
            if s!= self.initial_state and not self.get_incoming_transitions(s):
                disconnected = True
        return disconnected

    def get_missing_transitions(self, graph_before_merge, target_state, set_to_merge):
        missing_transitions = []
        for s in set_to_merge:
            incoming_transitions = graph_before_merge.get_incoming_transitions(s)
            for i_t in incoming_transitions:
                if not self.has_incoming_transition_label(target_state, i_t):
                    missing_transitions.append((s, i_t))
            outgoing_transitions = graph_before_merge.get_outgoing_transitions_for_state(s)
            for o_t in outgoing_transitions:
                if not self.has_outgoing_transition_for_label(target_state, o_t.label):
                    missing_transitions.append((s, o_t))
        return missing_transitions

    def print_map(self, map):
        for key, value in map.items():
            print(f"{key}: {value}")
        print('==================================================================')

    def map_to_string(self, map):
        map_str = ''
        for key, value in map.items():
            map_str += f"{key}: {value}\n"
        return map_str