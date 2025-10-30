from Learners.DFASAT.DFASAT_Variables import Z, X, YW
from Basic_objects.Graph import Graph
from Basic_objects.State import State
from Basic_objects.Transition import Transition


def get_model(sat_solution, variables_map, initial_state_in_partial_model):
    graph_dict = {}
    accepted_rejected_map = {}
    transition_map_temp = {}
    initial_state_color_id = None
    for variable, var_index in variables_map.items():
        if isinstance(variable, X) and variable.state_label == initial_state_in_partial_model.label and sat_solution[var_index-1]>0:
            graph_dict[State(label=variable.color_id, isInitial=True)] = {}
        elif isinstance(variable, Z):
            if sat_solution[var_index - 1] > 0:  #
                if State(label=variable.color_id) not in graph_dict.keys():
                    graph_dict[State(label=variable.color_id, type='accepted')] = {}
                else:
                    for state, dict in graph_dict.items():
                        if state.label == variable.color_id:
                            state.type = 'accepted'
                            break
            else:
                if State(label=variable.color_id) not in graph_dict.keys():
                    graph_dict[State(label=variable.color_id, type='rejected')] = {}
                else:
                    for state, dict in graph_dict.items():
                        if state.label == variable.color_id:
                            state.type = 'rejected'
                            break
        elif isinstance(variable, YW) and sat_solution[var_index-1] > 0:
            parent_state = None;    child_state = None
            input = variable.input; output = variable.output
            for state, dict in graph_dict.items():
                if state.label == variable.parent_color_id:
                    parent_state = state
                if state.label == variable.child_color_id:
                    child_state = state

            if not parent_state:
                parent_state = State(label=variable.parent_color_id)
                graph_dict[parent_state] = {}
            if not child_state:
                child_state = State(label=variable.child_color_id)
                graph_dict[child_state] = {}

            if parent_state not in graph_dict.keys():
                graph_dict[parent_state] = {child_state : [Transition(parent_state, child_state, input, output)]}
            elif child_state not in graph_dict[parent_state].keys():
                graph_dict[parent_state][child_state] = [Transition(parent_state, child_state, input, output)]
            else:
                graph_dict[parent_state][child_state].append(Transition(parent_state, child_state, input, output))
    return graph_dict

def dict_to_graph(model_dict, graph):#, sat_result, variables_map
    new_graph_obj = Graph()
    new_graph_obj.set_input_alphabet(graph.get_input_alphabet())
    new_graph_obj.set_output_alphabet(graph.get_output_alphabet())
    new_graph_obj.set_alphabet(graph.get_alphabet())
    new_graph_obj.graph = model_dict
    # set the initial state
    for state in model_dict.keys():
        if state.isInitial:
            new_graph_obj.set_initial_state(state)
            break
    # new_graph_obj.print_graph()

    return new_graph_obj