import re
from Learners.DFASAT.DFASAT_Variables import X, Z, YW
from write_clear_file import write_to_file_in_new_line

clauses_counter = 0
# Use this when the rejected state is the one with no out transitions
def build_formula_with_patterns(num_of_colors, graph, file_path, variables_map, exploration_map):
    global clauses_counter
    rejected_state_color = 1
    clauses_counter = build_formula(num_of_colors, graph, file_path, variables_map)
    for event, data in exploration_map.items():
        for non_follower in data.get('not_followed_by', []):
            clauses_list = b_should_not_follow_a(num_of_colors, variables_map, rejected_state_color, a=event, b=non_follower)
            write_to_file(f'c {non_follower}_should_not_follow_{event}\n', clauses_list, file_path)

    return clauses_counter

def build_formula(num_of_colors, graph, file_path,  variables_map):
    rejected_state_color = 1
    # 1- each state (red or non-red) must have exactly-1 color
    clauses_list = at_least_1_color(num_of_colors, graph, variables_map)
    write_to_file('c at_least_1_color', clauses_list, file_path)
    clauses_list = at_most_1_color(num_of_colors, graph, variables_map)
    write_to_file('c at_most_1_color', clauses_list, file_path)

    # 2- SYMMETRY BREAKING: each color either accepted or rejected
    clauses_list = separate_colors(num_of_colors, graph, variables_map, rejected_state_color)
    write_to_file('c separate_colors', clauses_list, file_path)

    # 3- if parent has color --> child has color
    clauses_list = child_colored_when_parent_colored(num_of_colors, graph, variables_map)
    write_to_file('c child_colored_when_parent_colored', clauses_list, file_path)

    # 4-  traget_1_accepted_state_per_input
    clauses_list = traget_1_accepted_state_per_input(num_of_colors, graph, variables_map, rejected_state_color)
    write_to_file('c traget_1_accepted_state_per_input', clauses_list, file_path)

    # 5- at_least_1_transition_from_any_state
    clauses_list = at_least_1_transition_per_input_from_any_state_except_rejected(num_of_colors, graph, variables_map, rejected_state_color)
    write_to_file('c at_least_1_transition_from_any_state', clauses_list, file_path)

    # clauses_list = at_most_1_transition_from_any_state_perInputOutputPair(num_of_colors, graph, variables_map, rejected_state_color)
    # write_to_file('c at_most_1_transition_from_any_state_perInputOutputPair', clauses_list, file_path)

    #  6- rejected_state_has_no_children
    clauses_list = rejected_state_has_no_children(num_of_colors, graph, variables_map, rejected_state_color)
    write_to_file('c rejected_state_has_no_children', clauses_list, file_path)

    return clauses_counter

def at_least_1_color(num_of_colors, graph, variables_map):
    clauses_list = []
    states = graph.get_all_states()
    for s in states:
        _clause_at_least_1 = ''
        for color_id in range(num_of_colors):
            current_variable = variables_map[X(s.label, color_id)]
            _clause_at_least_1 += f'{current_variable} '
        clauses_list.append(_clause_at_least_1)
    return clauses_list

def at_most_1_color(num_of_colors, graph, variables_map):
    clauses_list = []
    states = graph.get_all_states()
    for s in states:
        for color_id_1 in range(num_of_colors):
            current_variable_1 = variables_map[X(s.label, color_id_1)]
            for color_id_2 in range(color_id_1+1, num_of_colors):
                current_variable_2 = variables_map[X(s.label, color_id_2)]
                if current_variable_1 and current_variable_2:
                    _clause_at_most_1 = f'-{current_variable_1} -{current_variable_2} '
                    clauses_list.append(_clause_at_most_1)
    return clauses_list
#
# def exactly_1_color(num_of_colors, graph, variables_map):
#     clauses_list = []
#     global clauses_counter
#     states = graph.get_all_states()
#     for s in states:
#         _clause_at_most_1 = ''
#         _clause_at_least_1 = ''
#         for color_id in range(num_of_colors):
#             current_variable = variables_map[X(s.label, color_id)]
#             _clause_at_most_1 += f'-{current_variable} '
#             _clause_at_least_1 += f'{current_variable} '
#         clauses_list.append(_clause_at_most_1)
#         clauses_list.append(_clause_at_least_1)
#     return clauses_list

def at_least_1_transition_per_input_from_any_state_except_rejected(num_of_colors, graph, variables_map, rejected_state_color):
    # input enabled: each state (except the rejected one) must have
    # at least one outgoing transition for each input symbol going to a non-rejected state
    clauses_list = []
    for prnt_clr_id in range(num_of_colors):
        if prnt_clr_id == rejected_state_color:
            continue
        for input in graph.get_input_alphabet():
            _clause1 = ''
            for child_clr_id in range(num_of_colors):
                # if child_clr_id == rejected_state_color:
                #     continue
                for output in graph.get_output_alphabet():
                    current_variable = variables_map[YW(input, output, prnt_clr_id, child_clr_id)]
                    if current_variable:
                        _clause1 += f'{current_variable} '
            clauses_list.append(_clause1)
    return clauses_list

# def at_most_1_transition_from_any_state_perInputOutputPair(num_of_colors, graph, variables_map, rejected_state_color):
#     # deterministic: each state (except the rejected one) have
#     # at most one outgoing transition for each input/output pair
#     clauses_list = []
#     for prnt_clr_id in range(num_of_colors):
#         if prnt_clr_id == rejected_state_color:
#             continue
#         for input in graph.get_input_alphabet():
#
#             for output in graph.get_output_alphabet():
#                 for child_clr_id_1 in range(num_of_colors):
#
#                     current_variable_1 = variables_map[YW(input, output, prnt_clr_id, child_clr_id_1)]
#                     # for child_clr_id_2 in range(child_clr_id_1+1, num_of_colors):
#                     _clause1 = ''
#                         # if child_clr_id_1 == child_clr_id_2:
#                         #     continue
#                     current_variable_2 = variables_map[YW(input, output, prnt_clr_id, rejected_state_color)]
#                     if current_variable_2 and current_variable_1:
#                         _clause1 += f'-{current_variable_1} -{current_variable_2} '
#                         clauses_list.append(_clause1)
#     return clauses_list

def traget_1_accepted_state_per_input(num_of_colors, graph, variables_map, rejected_state_color):
    clauses_list = []
    for prnt_clr_id in range(num_of_colors):
        for input in graph.get_input_alphabet():
            for child_clr_id in range(num_of_colors):
                for output in graph.get_output_alphabet():
                    condition_YW_variable = variables_map[YW(input, output, prnt_clr_id, child_clr_id)]
                    condition_Z_variable = variables_map[Z(child_clr_id)]
                    #YW(load, 0, 0, 0) & Z(0) ⇒ ¬YW(load, 0, 0, RJ)
                    # consecuance_variable = variables_map[YW(input, output, prnt_clr_id, rejected_state_color)]
                    # _clause1 = f'-{condition_YW_variable} -{condition_Z_variable} -{consecuance_variable} '
                    # clauses_list.append(_clause1)
                    for other_output in graph.get_output_alphabet():
                        if other_output != output:
                            consecuance_variable = variables_map[YW(input, other_output, prnt_clr_id, rejected_state_color)]
                            if condition_YW_variable and condition_Z_variable and consecuance_variable:
                                # YW(load, 0, 0, 0) & Z(0) ⇒ YW(load, j, 0, RJ) & YW(load, j, 0, RJ) & YW(load, j, 0, RJ)
                                # where RJ == reject-state-color
                                # and    j != output_in_the_above_condition
                                _clause2 = f'-{condition_YW_variable} -{condition_Z_variable} {consecuance_variable} '
                                clauses_list.append(_clause2)
                    for other_child_clr_id in range(num_of_colors):
                        if other_child_clr_id != child_clr_id :
                            consecuance_variable = variables_map[YW(input, output, prnt_clr_id, other_child_clr_id)]
                            if condition_YW_variable and condition_Z_variable and consecuance_variable:
                                    # YW(load, 0, 0, 0) & Z(0) ⇒ ¬YW(load, 0, 0, 1) & ¬YW(load, 0, 0, 2) & ¬YW(load, 0, 0, k)
                                    # where k != current-child-color
                                    _clause = f'-{condition_YW_variable} -{condition_Z_variable} -{consecuance_variable} '
                                    clauses_list.append(_clause)
    return clauses_list


def separate_colors(num_of_colors, graph, variables_map, rejected_state_color):
    clauses_list = []
    for color_id in range(num_of_colors):
        _clause = ''
        current_variable_Z = variables_map[Z(color_id)]
        if color_id == rejected_state_color:
            _clause += f'-{current_variable_Z} '
        else:
            _clause += f'{current_variable_Z} '
        clauses_list.append(_clause)
    return clauses_list

def child_colored_when_parent_colored(num_of_colors, graph, variables_map):
    clauses_list = []
    transitions = graph.get_all_transitions()
    for t in transitions:
        for parent_color_id in range(num_of_colors):
            parent_variable = variables_map[X(t.from_state.label, parent_color_id)]
            for child_color_id in range(num_of_colors):
                child_variable = variables_map[X(t.to_state.label, child_color_id)]
                parent_relation_variable = variables_map[YW(t.input_key, t.output_key, parent_color_id, child_color_id)]
                if parent_variable and child_variable and parent_relation_variable:
                    #_clause1: A parent relation is set when a state and its parent are colored
                    # _clause2: A parent relation forces a state once the parent is colored
                    _clause1 = ''; _clause2 = ''
                    _clause1 = f'-{parent_variable} -{child_variable} {parent_relation_variable} '
                    _clause2 += f'-{parent_variable} {child_variable} -{parent_relation_variable} '
                    clauses_list.append(_clause1)
                    clauses_list.append(_clause2)
    return clauses_list


def b_should_not_follow_a(num_of_colors, variables_map, rejected_color, a, b):
    clauses_list = []
    _clause = ''
    a_input, a_output = split_input_output(a)
    b_input, b_output = split_input_output(b)

    for i in range(num_of_colors):
        if i == rejected_color:
            continue
        for j in range(num_of_colors):
            YW_a_i_j = variables_map[YW(a_input, a_output, i, j)]
            Z_j = variables_map[Z(j)]
            # if YW_a_i_j and Z_j:
            YW_b_j_RJ = variables_map[YW(b_input, b_output, j, rejected_color)]
            # for k in range(num_of_colors):
            #     _clause = ''
            #     if k == rejected_color:
            #         continue
            #     YW_b_j_k = variables_map[YW(b_input, b_output, j, k)]
                # Z_k = variables_map[Z(k)]
            if YW_a_i_j and Z_j and YW_b_j_RJ:
                _clause += f'-{YW_a_i_j} -{Z_j} {YW_b_j_RJ} '
                clauses_list.append(_clause)
    return clauses_list
    # clauses_list = []
    # _clause = ''
    # a_input, a_output = split_input_output(a)
    # b_input, b_output = split_input_output(b)
    #
    # for i in range(num_of_colors):
    #     for j in range(num_of_colors):
    #         YW_a_i_j = variables_map[YW(a_input, a_output, i, j)]
    #         Z_j = variables_map[Z(j)]
    #         if YW_a_i_j and Z_j:
    #             for k in range(num_of_colors):
    #                 _clause = ''
    #                 YW_b_j_k = variables_map[YW(b_input, b_output, j, k)]
    #                 Z_k = variables_map[Z(k)]
    #                 if YW_a_i_j and YW_b_j_k and Z_j and Z_k:
    #                     # YW(a_input, a_output, i, j) & Z(j) ⇒ ¬YW(b_input, b_output, j, k) or ¬Z(k)
    #                     _clause = f'-{YW_a_i_j} -{YW_b_j_k} -{Z_j} -{Z_k} '
    #                     clauses_list.append(_clause)
    # return clauses_list

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

def write_to_file(little_string, content_list, file_path):
    global clauses_counter
    with open(file_path, 'a') as f:
        f.write(f'{little_string}\n')
        for item in content_list:
            f.write(f"{item}0\n") #0 in minisat means end of clause
            clauses_counter += 1

def rejected_state_has_no_children(num_of_colors, graph, variables_map, rejected_state_color):
    clauses_list = []
    for child_color in range(num_of_colors):
        for _input in graph.get_input_alphabet():
            for _output in graph.get_output_alphabet():
                    current_variable = variables_map[YW(_input, _output, rejected_state_color, child_color)]
                    if current_variable:
                        # If the rejected state has a transition to another state, it should not be colored
                        clauses_list.append( f'-{current_variable} ')
    return clauses_list