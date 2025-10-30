from write_clear_file import write_to_file_in_new_line, clear_file


def explor_whatis_whatisnot_next(pta):
    alphabet = pta.G.get_alphabet()
    # transition_map = {'e1': [t1, t4], 'e2': [t3, t6, t7], 'e3': [t2, t5]}
    # transition_map : for alphabet character (transition label), list all traditions with that label
    transition_map_temp = {}

    # transition_map_final = {'e1':
    #                           {'follows_by': {'e3': 10, 'e6': 90},
    #                           'not_follows_by': ['e1', 'e2', 'e4', 'e5', 'e7'],
    #                           'percentage_of_appearance': 20
    #                           }
    #                           'e2':
    #                           {'follows_by': {'e1': 20, 'e3': 80},
    #                           'not_follows_by': ['e2', 'e4', 'e5', 'e6', 'e7'],
    #                           'percentage_of_appearance': 40
    #                           }
    #                     ....}
    # transition_map_final: for each alphabet character,
    # follows_by: list all characters that directly follows the key_character and their percentage of appearance
    # not_follows_by: list all characters that do not follow the key_character
    transition_map_final = {}
    for a in alphabet:
        transition_map_temp[a] = []
        transition_map_final[a] = {'followed_by': {}, 'not_followed_by': [], 'percentage_of_appearance': 0}

    # transition_map_temp: for alphabet character (transition label), list all transitions with that label
    for t in pta.G.get_all_transitions():
        transition_map_temp[f'{t.input_key}/{t.output_key}'].append(t)

    for a in transition_map_temp.keys():
        for t in transition_map_temp[a]:
            trans_follow_a = pta.G.get_outgoing_transitions_for_state(t.to_state)
            for ot in trans_follow_a:
                if ot.to_state.type == "accepted":
                    if f'{ot.input_key}/{ot.output_key}' not in transition_map_final[a]['followed_by']:
                        transition_map_final[a]['followed_by'][f'{ot.input_key}/{ot.output_key}'] = 1
                    else:
                        transition_map_final[a]['followed_by'][f'{ot.input_key}/{ot.output_key}'] +=1
        appearance_number_of_a = len(transition_map_temp[a])
        for k in alphabet:
            if k not in transition_map_final[a]['followed_by'].keys():
                transition_map_final[a]['not_followed_by'].append(k)

        for x in transition_map_final[a]['followed_by'].keys():
            transition_map_final[a]['followed_by'][x] = round((transition_map_final[a]['followed_by'][x]/appearance_number_of_a)*100,2)


        transition_map_final[a]['percentage_of_appearance'] = round((appearance_number_of_a / len(pta.G.get_all_transitions())) * 100,2)


    return transition_map_final

def hard_vs_soft_patterns(exploration_map):
    hard = {}
    soft = {}
    for event, data in exploration_map.items():
        if len(data['followed_by'].keys()) >=1:
            hard[event] = data
        else:
            soft[event] = data
    return hard, soft

def print_Exploration_map(exp_map):
    for event, data in exp_map.items():
        print(f"Event: {event}")

        print("  Followed by:")
        for follower, percent in data.get('followed_by', {}).items():
            print(f"    {follower}: {percent}%")

        print("  Not followed by:")
        for non_follower in data.get('not_followed_by', []):
            print(f"    {non_follower}")

        print(f"Percentage_of_appearance: {exp_map[event]['percentage_of_appearance']}%")
        print("-" * 30)

def save_Exploration_map_to_file(exp_map, file_path):
    clear_file(file_path)
    write_to_file_in_new_line(file_path, "Exploration Map")
    write_to_file_in_new_line(file_path, "=" * 30)
    for event, data in exp_map.items():
        write_to_file_in_new_line(file_path,f"Event: {event}")

        write_to_file_in_new_line(file_path,"  Followed by:")
        for follower, percent in data.get('followed_by', {}).items():
            write_to_file_in_new_line(file_path,f"    {follower}: {percent}%")

        write_to_file_in_new_line(file_path,"  Not followed by:")
        for non_follower in data.get('not_followed_by', []):
            write_to_file_in_new_line(file_path,f"    {non_follower}")

        write_to_file_in_new_line(file_path, f"Percentage_of_appearance: {exp_map[event]['percentage_of_appearance']}%")
        write_to_file_in_new_line(file_path,"-" * 30)
