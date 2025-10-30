import random

def generate_positive_walks(positive_walks_size, graph, seed_value):
    rng = random.Random(seed_value)
    # positive walks that are not neccessarily cover all transitions and states
    positive_walks = []
    while len(positive_walks) < positive_walks_size :
        walk = []
        current_state = graph.initial_state
        _continue = True
        while _continue:
            input_key = f'{rng.choice(graph.input_alphabet)}'
            transition = graph.get_outgoing_transitions_for_state_with_input(current_state, input_key)
            walk.append(f'{transition.input_key}/{transition.output_key}')
            current_state = graph.get_target_state(current_state, input_key)
            _continue = rng.uniform(0, 1) >= 0.5
        if walk not in positive_walks:
            positive_walks.append(walk)
    return positive_walks

def generate_prefixed_closed_negative_walks(negative_walks_size, graph, seed_value):
    rng = random.Random(seed_value)
    negative_walks = []
    while len(negative_walks) < negative_walks_size:
        walk = []
        current_state = graph.initial_state
        _continue = True
        while _continue:
            input_key = f'{rng.choice(graph.input_alphabet)}'
            output_key = graph.get_output(current_state, input_key)
            walk.append(f'{input_key}/{output_key}')
            current_state = graph.get_target_state(current_state, input_key)
            _continue = rng.uniform(0, 1) >= 0.5
        # generate the last transition that makes the walk negative. (add not exsitiing transition to the walk)
        input_key = f'{rng.choice(graph.input_alphabet)}'
        output_key = get_not_exist_output(current_state, input_key, graph, rng)
        walk.append(f'{input_key}/{output_key}')

        if walk not in negative_walks:
            negative_walks.append(walk)

    return negative_walks

def get_not_exist_output(state, input_key, graph, random_variable):
    actual_output_key = graph.get_output(state, input_key)
    output_list_exclude_actual_output = [output for output in graph.output_alphabet if output != actual_output_key]
    output_list_exclude_actual_output.sort()
    random_not_exist_output_key = f'{random_variable.choice(output_list_exclude_actual_output)}'
    return random_not_exist_output_key

def split_into_evaluation_and_training_lists(walks, evaluation_walks_size=30, seed=42):
    rng = random.Random(seed)
    walks_copy = walks[:]
    rng.shuffle(walks_copy)
    Evaluation_walks = walks_copy[:evaluation_walks_size]
    Training_walks = walks_copy[evaluation_walks_size:]
    return Training_walks, Evaluation_walks
    # rng = random.Random(seed)
    # Evaluation_walks = []
    # random_index_list = []
    # #evaluation_walks_size = int((evaluation_walks_size/100) * len(walks))
    # for i in range(evaluation_walks_size):
    #     random_index = rng.randint(0, len(walks) - 1)
    #     if random_index not in random_index_list:
    #         random_index_list.append(random_index)
    #         # add the evaluation traces
    #         Evaluation_walks.append(walks[random_index])
    #
    # Training_walks = []
    # for t in walks:
    #     if t not in Evaluation_walks:
    #         Training_walks.append(t)
    # # for i in range(len(walks) - 1):
    # #     # remove the evaluation traces
    # #     if i not in random_index_list:
    # #         Training_pos_walks.append(walks[i])
    #
    # return Training_walks,Evaluation_walks

def write_walks_to_file(training_pos_walks, training_neg_walks, test_pos_walks, test_neg_walks, filename):
    with open(filename, 'w') as file:
        file.write(f'__________Learning_Positive Traces_________\n')
        for walk in training_pos_walks:
            walk_str = to_sting_sperated_by_comma(walk)
            file.write(f'{walk_str}\n')
        file.write(f'__________Learning_Negative Traces_________\n')
        for walk in training_neg_walks:
            walk_str = to_sting_sperated_by_comma(walk)
            file.write(f'{walk_str}\n')
        file.write(f'__________EVALUATION_Positive Traces_________\n')
        for walk in test_pos_walks:
            walk_str = to_sting_sperated_by_comma(walk)
            file.write(f'{walk_str}\n')
        file.write(f'__________EVALUATION_Negative Traces_________\n')
        for walk in test_neg_walks:
            walk_str = to_sting_sperated_by_comma(walk)
            file.write(f'{walk_str}\n')

def to_sting_sperated_by_comma(walk):
    walk_str = ''
    for i in range(len(walk)):
        label = walk[i]
        walk_str += label
        if i != len(walk) - 1:
            walk_str += ', '
    return walk_str