import argparse
import time

from Basic_objects.Tree import Tree
from Form_converter.GraphObj_DotFile_converter import dot_to_Graph, graph_to_dot
from Learners.Baised_Learner import Baised_Learner
from Learners.DFASAT.SAT import SAT
from RandomWalksGenerator import generate_prefixed_closed_negative_walks, generate_positive_walks, \
    split_into_evaluation_and_training_lists
from evaluation import Evaluation
from write_clear_file import clear_file, write_to_file_in_new_line

def main():
    learning_strategy = 'BiasedAllRedSAT'
    parser = argparse.ArgumentParser(description="Process seed, file name, and trail count.")
    parser.add_argument("seed", type=int, help="Integer seed value")
    parser.add_argument("output_directory", type=str, help="output directory")
    parser.add_argument("systemName", type=str, help="Input file name")
    parser.add_argument("trails", type=int, help="Number of trails")
    parser.add_argument("walks_size", type=int, help="Number of positive and negative walks to generate")

    args = parser.parse_args()

    output_directory = args.output_directory
    systemName = args.systemName
    trails = args.trails
    walks_size = args.walks_size
    seed_value = args.seed

    statistic_file_path = f'{systemName}/{output_directory}/{systemName}_{trails}_{walks_size}_{learning_strategy}_statistics.txt'
    # Read Reference graph
    ref_graph = dot_to_Graph(f'reference_automata/{systemName}_reference.dot')
    ref_graph.input_alphabet.sort()
    clear_file(statistic_file_path)
    write_to_file_in_new_line(statistic_file_path,
                              f'File: {systemName}\n'
                              f'Seed: {seed_value}\n'
                              f'Trails: {trails}\n'
                              f'Number of walks: {walks_size}\n'
                              f'Size of reference graph: {len(ref_graph.get_all_states())} states\n'
                              f'Alphabet_size: {len(ref_graph.alphabet)} symbols\n')
    # Generate walks
    pos_walks = []
    neg_walks = generate_prefixed_closed_negative_walks(walks_size, ref_graph, seed_value * 2)

    training_pos_walks = []
    test_pos_walks = generate_positive_walks(int(walks_size * 0.66), ref_graph, seed_value)
    training_neg_walks, test_neg_walks = split_into_evaluation_and_training_lists(neg_walks, int(walks_size * 0.66),
                                                                                  seed_value)
    # Read EDSM result graph
    G = dot_to_Graph(f'{systemName}/BiasedEDSM/{systemName}_{trails}_{walks_size}_BiasedEDSM.dot')
    apta = Tree()
    apta.G = G
    edsm = Baised_Learner(apta)

    # Run SAT
    total_sat_time = 0.0
    start_time = time.time()
    sat_solver = SAT(edsm.pta.G)
    dfasat_graph = sat_solver.run_dfasat(f'{systemName}/{output_directory}/{systemName}_{trails}_{walks_size}_{learning_strategy}')
    total_sat_time += time.time() - start_time
    sat_solver.write_dfasat_report(statistic_file_path)
    write_to_file_in_new_line(statistic_file_path,
                              f'Total time spent in SAT solver (seconds): {total_sat_time:.4f}\n')
    if dfasat_graph:
        graph_to_dot(dfasat_graph, f'{systemName}/{output_directory}/{systemName}_{trails}_{walks_size}_{learning_strategy}.dot')
        edsm.pta.G = dfasat_graph
        # Evaluate the learned graph
        eval = Evaluation(edsm, test_pos_walks, test_neg_walks)
        true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, Accuracy, BCR = eval.evaluate()
        eval.write_evaluation_report(statistic_file_path,
                                     true_positive, true_negative, false_positive, false_negative,
                                     precision, recall, specificity, F_measure, Accuracy, BCR)



if __name__ == "__main__":
    main()
