# import re
import pydot
from Basic_objects.State import State
from Basic_objects.Transition import Transition
from Basic_objects.Graph import Graph

def dot_to_Graph(dot_file_path):
    # Parse the DOT file
    graphs = pydot.graph_from_dot_file(dot_file_path)
    graph = graphs[0]

    # Create a dictionary to hold the states and transitions
    graph_dictionary = {}

    # Initialize the Graph object
    graph_obj = Graph()

    # Initialize sets for input and output alphabets
    input_alphabet = set()
    output_alphabet = set()
    alphabet = set()

    # Create State objects for each node
    for node in graph.get_nodes():
        name = node.get_name().strip('"') #strip('"'): remove double quotes
        if name in ('node', 'graph', 'edge'):  # Skip global settings
            continue
        label = node.get_label().strip('"') if node.get_label() else name
        state = State(label=label)

        # Set color if defined
        fillcolor = node.get_fillcolor()
        if fillcolor:
            if fillcolor.strip('"') == "red":
                state.color = "red"
            else:
                state.color = "white"  # default
        # Set the initial state
        isInitial = node.get_attributes().get('isInitial', 'false').lower() == 'true'
        if isInitial:
            state.isInitial = True
            graph_obj.set_initial_state(state)
        else:
            state.isInitial = False

        graph_dictionary[state] = {}

    # Create Transition objects for each edge and extract input/output
    for edge in graph.get_edges():
        from_state = get_state_by_label(graph_dictionary, edge.get_source().strip('"'))
        to_state = get_state_by_label(graph_dictionary, edge.get_destination().strip('"'))
        label = edge.get_label().strip('"')


        #split the label into input and output symbols when "/" is present (e.g., "a / b" => "a", "b")(e.g., "a/b" => "a", "b")
        input_output_list = split_into_input_output(label)
        for input_symbol, output_symbol in input_output_list:
            input_key = graph_obj.add_to_input_map(input_symbol)
            input_alphabet.add(input_symbol)

            output_key = graph_obj.add_to_output_map(output_symbol)
            output_alphabet.add(output_symbol)

            transition = Transition(from_state, to_state, input_symbol, output_symbol)
            alphabet.add(f'{transition.input_key}/{transition.output_key}')
            if from_state not in graph_dictionary:
                graph_dictionary[from_state] = {}
            if to_state not in graph_dictionary[from_state]:
                graph_dictionary[from_state][to_state] = []
            graph_dictionary[from_state][to_state].append(transition)

    # Set the graph dictionary in the Graph object
    graph_obj.graph = graph_dictionary
    # Set the input and output alphabets in the Graph object
    graph_obj.set_input_alphabet(list(input_alphabet))
    graph_obj.set_output_alphabet(list(output_alphabet))
    graph_obj.set_alphabet(list(alphabet))

    return graph_obj

def get_state_by_label(graph_dict, label):
    for state in graph_dict.keys():
        if state.label == label:
            return state
    return None  # If not found

def split_into_input_output(label):
    # Replace literal \n with actual newlines
    label = label.replace('\\n', '\n')
    # Split by newline to get each part
    parts = label.strip().split('\n')
    pairs = []
    for part in parts:
        input_symbol, output_symbol = [s.strip() for s in part.split('/', maxsplit=1)]
        pairs.append([input_symbol, output_symbol])
    return pairs

def graph_to_dot(graph: Graph, filename="output.dot"):
    lines = []
    lines.append("digraph G {")
    lines.append("  rankdir=LR;")  # Left-to-right layout
    lines.append('  node [shape=circle, style=filled, fillcolor=white];')

    for state in graph.get_all_states():
        attrs = []
        # Color and shape adjustments
        if state == graph.initial_state:#state.isInitial:
            attrs.append('isInitial=True')
            attrs.append('fillcolor=lightblue')
        elif state.color == 'red':
            attrs.append('fillcolor=red')
        elif state.color == 'blue':
            attrs.append('fillcolor=blue')
        elif state.color == 'yellow':
            attrs.append('fillcolor=yellow')
        if state.type == 'accepted':
            attrs.append('shape=doublecircle')
        elif state.type == 'rejected':
            attrs.append('shape=square')

        lines.append(f'  "{state.label}" [{", ".join(attrs)}];')

    for from_state, to_states in graph.graph.items():
        edge_labels = {}  # collect multiple labels for same edge
        for to_state, transitions in to_states.items():
            label = "\\n".join([t.label for t in transitions])
            lines.append(f'  "{from_state.label}" -> "{to_state.label}" [label="{label}"];')

    lines.append("}")
    dot_output = "\n".join(lines)

    with open(filename, 'w') as f:
        f.write(dot_output)

    return dot_output
