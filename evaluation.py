import re

class Evaluation:
    def __init__(self, learned_graph, accepted_traces, rejected_traces): #learned_graph:Learner
        self.G = learned_graph.pta.G
        self.pta_obj = learned_graph.pta
        self.positive_traces = accepted_traces
        self.negative_traces = rejected_traces
        # self.split_dataset(accepted_traces, rejected_traces)

    def is_trace_in_G(self, trace): # trace is a set of strings ['a','a', 'b', 'x']
        s = self.G.initial_state
        for label in trace:
            input_key , output_key = self.split_input_output(label)
            s = self.G.get_target_state_for_label(s, input_key, output_key)
            if not s:
                return False, ""
        return True, s.type

    def split_input_output(self, label):
        match = re.search(r'\s*/\s*', label)
        if match:
            input_end = match.start()
            output_start = match.end()
            _input = label[:input_end]
            _output = label[output_start:]
            return _input, _output
        return None, None

    def evaluate(self):
        true_positive =0
        false_positive = 0
        true_negative = 0
        false_negative = 0

        true_positive_lsit = []
        false_positive_list = []
        true_negative_list = []
        false_negative_list = []
        for trace in self.positive_traces:
            # print(trace)
            result, lastStateType = self.is_trace_in_G(trace)
            if result and (lastStateType == "accepted" or lastStateType == "unlabeled") :
                true_positive +=1
                true_positive_lsit.append(trace)
            else:
                false_negative +=1
                false_negative_list.append(trace)

        for trace in self.negative_traces:
            # print(trace)
            # result = self.is_trace_in_G(trace)
            result, lastStateType = self.is_trace_in_G(trace)
            if result and (lastStateType == "accepted" or lastStateType == "unlabeled"):
                false_positive += 1
                false_positive_list.append(trace)
            elif not result or lastStateType=="rejected":
                true_negative += 1
                true_negative_list.append(trace)
        if true_positive+false_positive == 0:
            precision = 0
            specificity = 0
        else:
            precision = true_positive/(true_positive+false_positive)
            specificity = true_negative/(true_negative+false_positive)
        if true_positive+false_negative == 0:
            recall = 0
        else:
            recall = true_positive / (true_positive + false_negative)
        if precision+recall == 0:
            F_measure = 0
        else:
            F_measure = round((2*precision*recall)/(precision+recall),1)
        Accuracy = round((true_positive + true_negative) / (len(self.positive_traces) + len(self.negative_traces)),1)
        BCR = round(0.5 * (recall+specificity),1)

        return true_positive, true_negative, false_positive, false_negative, precision, recall, specificity, F_measure, Accuracy, BCR

    def print_lst(self, lst):
        for item in lst:
            print(item)

    def write_evaluation_report(self, filename, true_positive, true_negative, false_positive, false_negative,
                                     precision, recall, specificity, F_measure, Accuracy, BCR):
        with open(filename, 'a') as f:
            f.write('\n')
            f.write('Evaluation Report:\n')
            f.write(f'number of Positive traces: {len(self.positive_traces)}\n')
            f.write(f'number of Negative traces: {len(self.negative_traces)}\n')
            f.write(f'True Positive: {true_positive}\n')
            f.write(f'True Negative: {true_negative}\n')
            f.write(f'False Positive: {false_positive}\n')
            f.write(f'False Negative: {false_negative}\n')
            f.write(f'Precision: {precision:.2f}\n')
            f.write(f'Recall: {recall:.2f}\n')
            f.write(f'Specificity: {specificity:.2f}\n')
            f.write(f'F-measure: {F_measure:.2f}\n')
            f.write(f'Accuracy: {Accuracy:.2f}\n')
            f.write(f'BCR: {BCR:.2f}\n')
