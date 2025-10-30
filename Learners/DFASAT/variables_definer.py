import re
from Learners.DFASAT.DFASAT_Variables import Z, X, YW

variables_counter = 0
variables_map = {}

def set_variables(number_of_colors, graph):
    global variables_counter, variables_map
    variables_counter = 0; variables_map = {}
    #1- variables for coloring every state
    build_variables_color_for_every_state(number_of_colors, graph)
    #2- variables for accepted/rejected colors
    build_variables_accepted_rejected_colors(number_of_colors)
    #3- variables for parent_relation
    build_variables_parent_relation(number_of_colors, graph)
    return variables_map

def build_variables_color_for_every_state(num_of_colors, graph):
    global variables_counter, variables_map
    states = graph.get_all_states()
    for s in states:
        for color_id in range(num_of_colors):
            if X(s.label, color_id) not in variables_map.keys():
                variables_counter += 1
                variables_map[X(s.label, color_id)] = variables_counter
    return variables_map


def build_variables_accepted_rejected_colors(number_of_colors):
    global variables_counter, variables_map
    for color_id in range(number_of_colors):
            if Z(color_id) not in variables_map.keys():
                variables_counter += 1
                variables_map[Z(color_id)] = variables_counter
    return variables_map

def build_variables_parent_relation(num_of_colors, graph):
    global variables_counter, variables_map
    # alphabet = graph.get_alphabet()
    inputs = graph.get_input_alphabet()
    outputs = graph.get_output_alphabet()
    for i in inputs:
        # _input, _output  = split_input_output(a)
        for o in outputs:
            for parent_color_id in range(num_of_colors):
                for child_color_id in range(num_of_colors):
                    if YW(i, o, parent_color_id, child_color_id) not in variables_map.keys():
                        variables_counter += 1
                        variables_map[YW(i, o, parent_color_id, child_color_id)] = variables_counter
    return variables_map

def split_input_output(label):
    match = re.search(r'\s*/\s*', label)
    _input = None
    _output = None
    if match:
        input_end = match.start()
        output_start = match.end()
        _input = label[:input_end]
        _output = label[output_start:]
    return _input, _output