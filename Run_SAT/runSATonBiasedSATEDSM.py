import os
import re
from Form_converter.GraphObj_DotFile_converter import dot_to_Graph, graph_to_dot
from Learners.DFASAT.variables_definer import set_variables
from Learners.DFASAT.visualizer import get_model, dict_to_graph


def getSATDotFile(num_of_colors, directory, prefix,learning_strategy):
    sat_result = getSATResult(f'{directory}/{prefix}{learning_strategy}_SAT_result.txt')
    graph = dot_to_Graph(f'{directory}/{prefix}{learning_strategy}EDSM.dot')

    variables_map = set_variables(num_of_colors, graph)
    model_dict = get_model(sat_result, variables_map, graph.get_initial_state())
    dfasat_graph = dict_to_graph(model_dict, graph)#, sat_result
    graph_to_dot(dfasat_graph, f'{directory}/{prefix}{learning_strategy}.dot')

def getSATResult(output_file):
    with open(output_file, 'r') as f:
        lines = f.readlines()

    if not lines:
        return "Unknown error or empty result"

    if lines[0].strip() == "UNSAT":
        return "UNSAT"
    elif lines[0].strip() == "SAT":
        model = list(map(int, lines[1].split()))
        # Filter out the zero at the end
        model = [v for v in model if v != 0]
        return model




if __name__ == "__main__":
    directory = 'result/BiasedSAT'
    learning_strategy = 'BiasedSAT'
    prefix='coffeemachine_0_2000_'
    getSATDotFile(7, directory, prefix, learning_strategy)
    # directory = 'result/BiasedSAT'
    # learning_strategy = 'BiasedSAT'
    #
    # for file in os.listdir(directory):
    #     if file.endswith('result.txt'):
    #         # Extract prefix up to the third underscore
    #         match = re.match(r'(.*?_[^_]*_[^_]*_)', file)
    #         if match:
    #             prefix = match.group(1)
    #             stats_file = f"{prefix}{learning_strategy}_statistics.txt"
    #             stats_path = os.path.join(directory, stats_file)
    #             if os.path.exists(stats_path):
    #                 with open(stats_path, 'r') as sf:
    #                     for line in sf:
    #                         if 'Number of colors used (automata_size):' in line:
    #                             number_of_colors = int(line.split(':')[-1].strip())
    #                             break
    #                     else:
    #                         continue  # Skip if not found
    #                 getSATDotFile(number_of_colors, directory, prefix, learning_strategy)