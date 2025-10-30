import os

def retrieve_traces(file_name):
    learning_positive_traces = []
    learning_negative_traces = []
    evaluation_positive_traces = []
    evaluation_negative_traces = []

    with open(file_name, 'r') as file:
        current_section = None
        for line in file:
            line = line.strip()
            if line == '__________Learning_Positive Traces_________':
                current_section = 'learning_positive'
            elif line == '__________Learning_Negative Traces_________':
                current_section = 'learning_negative'
            elif line == '__________EVALUATION_Positive Traces_________':
                current_section = 'evaluation_positive'
            elif line == '__________EVALUATION_Negative Traces_________':
                current_section = 'evaluation_negative'
            elif current_section and line:
                trace = [label.strip() for label in line.split(', ') if label.strip()]
                if current_section == 'learning_positive':
                    learning_positive_traces.append(trace)
                elif current_section == 'learning_negative':
                    learning_negative_traces.append(trace)
                elif current_section == 'evaluation_positive':
                    evaluation_positive_traces.append(trace)
                elif current_section == 'evaluation_negative':
                    evaluation_negative_traces.append(trace)

    return learning_positive_traces, learning_negative_traces, evaluation_positive_traces, evaluation_negative_traces


if __name__ == '__main__':
    directory = 'Traces'
    all_files = os.listdir(directory)

    for file_name in all_files:
        if file_name.endswith('_Traces.txt'):
            full_path = os.path.join(directory, file_name)
            print(f'Processing file: {full_path}')
            learning_pos, learning_neg, eval_pos, eval_neg = retrieve_traces(full_path)
            print(f'Learning Positive Traces: {len(learning_pos)}')
            print(f'Learning Negative Traces: {len(learning_neg)}')
            print(f'Evaluation Positive Traces: {len(eval_pos)}')
            print(f'Evaluation Negative Traces: {len(eval_neg)}')
            print('---------------------------------')