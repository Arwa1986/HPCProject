def bias_merging_score (ds, exp_map, graph_after_merge):

    sets = ds.get_sets()
    for target, sources in sets.items():
        if len(sources) > 1:
            in_trans = graph_after_merge.get_incoming_transitions(target)
            out_trans = graph_after_merge.get_outgoing_transitions_for_state(target)

            for it in in_trans:
                if it.label in exp_map.keys():
                    for ot in out_trans:
                        # if ot.label in exp_map[it.label]['followed_by'].keys():
                        #     increase_score(ds, exp_map[it.label]['followed_by'][ot.label])
                        if ot.label in exp_map[it.label]['not_followed_by'] and ot.to_state.type == ('accepted'):
                            decrease_score(ds, exp_map[it.label]['percentage_of_appearance'])


# def increase_score(ds, percentage):
#     if ds.merging_score == 0:
#         INCREASE_BY = round(1 * (percentage / 100), 2)
#     else:
#         INCREASE_BY = round(ds.merging_score *(percentage/100), 2)
#     ds.biased_by +=INCREASE_BY

def decrease_score(ds, percentage):
    if ds.merging_score == 0:
        DECREASE_BY = round(1 * (percentage / 100), 2)
    else:
        DECREASE_BY = round(ds.merging_score * (percentage / 100), 2)
    ds.biased_by -= DECREASE_BY

def is_violate_pattern(ds, pattern_map, graph_after_merge):
    sets = ds.get_sets()
    for target, sources in sets.items():
        if len(sources) > 1:
            in_trans = graph_after_merge.get_incoming_transitions(target)
            out_trans = graph_after_merge.get_outgoing_transitions_for_state(target)

            for it in in_trans:
                if it.label in pattern_map.keys():
                    for ot in out_trans:
                        if ot.label in pattern_map[it.label]['not_followed_by'] and ot.to_state.type == ('accepted'):
                            return True, it.label
    return False, None