import argparse
import time

from Form_converter.GraphObj_DotFile_converter import dot_to_Graph, graph_to_dot
from Learners.Classical_Learner import Learner
from RandomWalksGenerator import generate_positive_walks, generate_prefixed_closed_negative_walks, \
    split_into_evaluation_and_training_lists, write_walks_to_file
from Basic_objects.Tree import Tree
from evaluation import Evaluation
from write_clear_file import write_to_file_in_new_line, clear_file


def main():
    learning_strategy = 'classicalEDSM'
    parser = argparse.ArgumentParser(description="Process seed, file name, and trail count.")
    parser.add_argument("seed", type=int, help="Integer seed value")
    parser.add_argument("directory", type=str, help="Input directory")
    parser.add_argument("filename", type=str, help="Input file name")
    parser.add_argument("trails", type=int, help="Number of trails")
    parser.add_argument("walks_size", type=int, help="Number of positive and negative walks to generate")

    args = parser.parse_args()
    statistic_file_path = f'{args.directory}/{args.filename}_{args.trails}_{args.walks_size}_{learning_strategy}_statistics.txt'
    # Read Reference graph
    ref_graph = dot_to_Graph(f'Traces/{args.filename}_reference.dot')
    ref_graph.input_alphabet.sort()
    clear_file(statistic_file_path)
    write_to_file_in_new_line(statistic_file_path,
                              f'File: {args.filename}\nSeed: {args.seed}\nTrails: {args.trails}\nNumber of walks: {args.walks_size}\n'
                              f'Size of reference graph: {len(ref_graph.get_all_states())} states\n'
                              f'Alphabet_size: {len(ref_graph.alphabet)} symbols\n')
    # Generate walks
    seed_value = args.seed
    pos_walks = generate_positive_walks(args.walks_size, ref_graph, seed_value)
    neg_walks = generate_prefixed_closed_negative_walks(args.walks_size, ref_graph, seed_value * 2)

    training_pos_walks, test_pos_walks = split_into_evaluation_and_training_lists(pos_walks, 30, seed_value)
    training_neg_walks, test_neg_walks = split_into_evaluation_and_training_lists(neg_walks, 30, seed_value)
    write_walks_to_file(training_pos_walks, training_neg_walks, test_pos_walks, test_neg_walks,
                        f'{args.directory}/{args.filename}_{args.trails}_{args.walks_size}_traces.txt')
    # Build APTA
    apta = Tree()
    apta.build_labeled_tree(ref_graph, training_pos_walks, training_neg_walks)
    graph_to_dot(apta.G, filename=f"{args.directory}/{args.filename}_{args.trails}_{args.walks_size}_apta.dot")

    # RUN classical EDSM
    total_edsm_time = 0.0
    start_time = time.time()
    classical_edsm = Learner(apta)
    classical_edsm.setup(f'{args.directory}/{args.filename}_{args.trails}_{args.walks_size}_{learning_strategy}_mergeTracker.txt')
    rejected_state = classical_edsm.mergre_rejected_states()
    classical_edsm.run_EDSM_learner()
    total_edsm_time += time.time() - start_time
    classical_edsm.write_statistics(statistic_file_path)
    write_to_file_in_new_line(statistic_file_path,
                              f'Total time spent in EDSM (seconds): {total_edsm_time:.4f}\n')
    graph_to_dot(classical_edsm.pta.G,f'{args.directory}/{args.filename}_{args.trails}_{args.walks_size}_{learning_strategy}.dot')

    # Evaluate the learned graph
    eval = Evaluation(classical_edsm, test_pos_walks, test_neg_walks)
    true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, Accuracy, BCR = eval.evaluate()
    eval.write_evaluation_report(statistic_file_path,
                                     true_positive, true_negative, false_positive, false_negative,
                                     precision, recall, specificity, F_measure, Accuracy, BCR)

if __name__ == '__main__':
    main()