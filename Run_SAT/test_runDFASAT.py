import time

from Form_converter.GraphObj_DotFile_converter import dot_to_Graph, graph_to_dot
from Learners.Baised_Learner import Baised_Learner
from Learners.DFASAT.SAT import SAT
from Patterns.pattern_from_traces.Explore_PTA import explor_whatis_whatisnot_next, save_Exploration_map_to_file, \
    hard_vs_soft_patterns
from RandomWalksGenerator import generate_positive_walks, generate_prefixed_closed_negative_walks, \
    split_into_evaluation_and_training_lists, write_walks_to_file
from Basic_objects.Tree import Tree
from evaluation import Evaluation
from retrive_traces import retrieve_traces
from write_clear_file import write_to_file_in_new_line, clear_file

if __name__=="__main__":
    directory= 'Traces_test'; filename= '../coffeemachine'; seed=42; trails=0; walks_size=500
    # Read Reference graph
    ref_graph = dot_to_Graph(f'{directory}/{filename}_reference.dot')
    ref_graph.input_alphabet.sort()
    clear_file(f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM_statistics.txt')
    write_to_file_in_new_line(
        f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM_statistics.txt',
        f'file: {filename}\nTrails: {trails}\nNumber of walks: {walks_size}\n'
        f'Size of reference graph: {len(ref_graph.get_all_states())} states\n'
        f'Alphabet_size: {len(ref_graph.input_alphabet)} symbols\n')
    seed_value = seed
    # retrieve previously generated walks from file
    training_pos_walks, training_neg_walks, test_pos_walks, test_neg_walks = retrieve_traces(
        f'{directory}/{filename}_{trails}_{walks_size}_classicalEDSM_traces.txt')
    # Build APTA
    apta = Tree()
    apta.build_labeled_tree(ref_graph, training_pos_walks, training_neg_walks)

    # RUN classical EDSM
    total_edsm_time = 0.0
    start_time = time.time()
    edsm = Baised_Learner(apta)
    edsm.setup(f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM_mergeTracker.txt')
    save_Exploration_map_to_file(edsm.hard_patterns,
                                 f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM_hard_map.txt')
    save_Exploration_map_to_file(edsm.soft_patterns,
                                 f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM_soft_map.txt')
    rejected_state = edsm.mergre_rejected_states()
    edsm.run_EDSM_with_pattern_learner()
    total_edsm_time += time.time() - start_time
    edsm.write_statistics(f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM_statistics.txt')
    write_to_file_in_new_line(
        f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM_statistics.txt',
        f'Total time spent in EDSM (seconds): {total_edsm_time:.4f}\n')
    graph_to_dot(edsm.pta.G, f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM.dot')

    # Evaluate the learned graph
    eval = Evaluation(edsm, test_pos_walks, test_neg_walks)
    true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, Accuracy, BCR = eval.evaluate()
    eval.write_evaluation_report(
        f'{directory}/{filename}_{trails}_{walks_size}_BaisedEDSM_statistics.txt',
        true_positive, true_negative, false_positive, false_negative,
        precision, recall, specificity, F_measure, Accuracy, BCR)
