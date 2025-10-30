import copy

from Patterns.pattern_from_traces.Explore_PTA import hard_vs_soft_patterns, explor_whatis_whatisnot_next
from Patterns.pattern_from_traces.check_after_merge import is_violate_pattern, decrease_score
from Basic_objects.DISJOINTSETS import DisjointSet
from write_clear_file import write_to_file_in_new_line


class Baised_Learner:
    figure_num = 2
    def __init__(self, pta):
        self.pta = pta
        self.found_blue = False
        self.visited = []
        self.blue_states = []


    def setup(self, with_pattern_file_name):
        self.pta.G.initial_state.color = 'red'
        self.red_states = [self.pta.G.initial_state]
        self.make_children_blue(self.pta.G.initial_state)
        self.correct_merge_counter = 0
        self.incorrect_merge_counter = 0
        self.with_pattern_file_name = with_pattern_file_name
        self.sizeof_actual_system = len(self.pta.G.graph.keys())
        self.exploration_map = explor_whatis_whatisnot_next(self.pta)
        self.hard_patterns, self.soft_patterns = hard_vs_soft_patterns(self.exploration_map)
        self.merge_blocked_by_pattern = 0
        self.merge_biased_by_pattern = 0



    def is_all_states_red(self):
        state_list = list(self.pta.G.graph.keys())
        for s in state_list:
            if s.color != 'red':
                return False
        return True


    def run_EDSM_with_pattern_learner(self):
        if self.is_all_states_red():
            return

        self.found_blue = False
        self.blue_states = []
        self.visited = []
        self.update_blue_states()
        # write_to_file_in_new_line(self.with_pattern_file_name, f'BLUE_STATES: {self.blue_states}')

        # mergable_states is  a list contains all pairs of state that are valid to be merged with their merging scour
        mergable_states=[]
        blue=None
        valid_for_at_least_one_red = False
        for blue in self.blue_states:
            # write_to_file_in_new_line(self.with_pattern_file_name, f'RED_STATES: {self.red_states}')
            for red in self.red_states:
                # Create a new disjoint set data structure
                ds = DisjointSet()
                ds.s1 = red
                ds.s2 = blue
                self.make_set_for_every_state_rooted_at(ds, red)
                self.make_set_for_every_state_rooted_at(ds, blue)

                work_to_do = {}

                add_new_state = ds.union(red, blue)
                work_to_do[ds.find(red)] = ds.get_set(red)
                if add_new_state:
                    self.compute_classes2(ds, work_to_do)

                if self.is_valid_merge(ds): # and not violate_hard_pattern(pattern_list, self.pta.G):
                    ds.merging_score = self.compute_score_accepted_states(ds)
                    # make a copy of the learner to check if the merge is valid with the patterns
                    # the actual merge will be done on the copy and the original will remain unchanged
                    # this way we don't have to unmerge. we just discard the copy
                    temp_learner = copy.deepcopy(self)
                    temp_learner.try_to_merge_sets(ds)

                    # write_to_file_in_new_line(self.with_pattern_file_name,f'Merging {ds.s1} & {ds.s2} => score: {ds.merging_score}' )
                    violate_hard_pattern, violated_hard_label = is_violate_pattern(ds, self.hard_patterns, temp_learner.pta.G)
                    violate_soft_pattern, violated_soft_label = is_violate_pattern(ds, self.soft_patterns, temp_learner.pta.G)
                    if violate_hard_pattern:
                        ds.merging_score = -1
                        # write_to_file_in_new_line(self.with_pattern_file_name,
                        #                           f'Blocked => score: {ds.merging_score}')
                        self.merge_blocked_by_pattern +=1
                    elif violate_soft_pattern:
                        decrease_score(ds, self.soft_patterns[violated_soft_label]['percentage_of_appearance'])
                        ds.biased_score = ds.merging_score + ds.biased_by
                        # write_to_file_in_new_line(self.with_pattern_file_name, f'= > bisaed_score: {ds.biased_score}')
                        self.merge_biased_by_pattern +=1
                    else:
                        ds.biased_score = ds.merging_score

                    if ds.biased_score > 0:
                            mergable_states.append(ds)
                            valid_for_at_least_one_red = True
                else:
                    ds.merging_score = -1
                    # write_to_file_in_new_line(self.with_pattern_file_name,f'Merging {ds.s1} & {ds.s2} => score: {ds.merging_score}' )

            if not valid_for_at_least_one_red:
                 # the blue_state can't be merged with any red_state
                self.make_it_red(blue)
                self.make_children_blue(blue)
                break

        if valid_for_at_least_one_red:
            ds_with_highest_scour = self.pick_high_biased_score_pair(mergable_states) #self.pick_pair_with_least_biase(mergable_states)
            # write_to_file_in_new_line(self.with_pattern_file_name, '*' * 30)
            # write_to_file_in_new_line(self.with_pattern_file_name, f'{ds_with_highest_scour.s1} & {ds_with_highest_scour.s2} has the highest scour : {ds_with_highest_scour.biased_score}')

            if ds_with_highest_scour.s1.get_reference_state() != ds_with_highest_scour.s2.get_reference_state():
                # write_to_file_in_new_line(self.with_pattern_file_name, f'Incorrect merge: {ds_with_highest_scour.s1} & {ds_with_highest_scour.s2}')
                self.incorrect_merge_counter += 1
            else:
                self.correct_merge_counter += 1
            # write_to_file_in_new_line(self.with_pattern_file_name, '*' * 30)
            self.merge_sets(ds_with_highest_scour)

        self.update_red_states()
        self.run_EDSM_with_pattern_learner()

    def run_EDSM_with_pattern_learner_partial_merger(self):
        total_number_of_merges = self.correct_merge_counter+self.incorrect_merge_counter
        #total_number_of_merges>=4:
        if self.is_all_states_red() or len(self.pta.G.get_all_states()) <= (self.sizeof_actual_system/2):
            return

        self.found_blue = False
        self.blue_states = []
        self.visited = []
        self.update_blue_states()
        # write_to_file_in_new_line(self.with_pattern_file_name, f'BLUE_STATES: {self.blue_states}')

        # mergable_states is  a list contains all pairs of state that are valid to be merged with their merging scour
        mergable_states = []
        blue = None
        valid_for_at_least_one_red = False
        for blue in self.blue_states:
            # write_to_file_in_new_line(self.with_pattern_file_name, f'RED_STATES: {self.red_states}')
            for red in self.red_states:
                # Create a new disjoint set data structure
                ds = DisjointSet()
                ds.s1 = red
                ds.s2 = blue
                self.make_set_for_every_state_rooted_at(ds, red)
                self.make_set_for_every_state_rooted_at(ds, blue)

                work_to_do = {}

                add_new_state = ds.union(red, blue)
                work_to_do[ds.find(red)] = ds.get_set(red)
                if add_new_state:
                    self.compute_classes2(ds, work_to_do)

                if self.is_valid_merge(ds):  # and not violate_hard_pattern(pattern_list, self.pta.G):
                    ds.merging_score = self.compute_score_accepted_states(ds)
                    # make a copy of the learner to check if the merge is valid with the patterns
                    # the actual merge will be done on the copy and the original will remain unchanged
                    # this way we don't have to unmerge. we just discard the copy
                    temp_learner = copy.deepcopy(self)
                    temp_learner.try_to_merge_sets(ds)

                    # write_to_file_in_new_line(self.with_pattern_file_name,
                    #                           f'Merging {ds.s1} & {ds.s2} => score: {ds.merging_score}')
                    violate_hard_pattern, violated_hard_label = is_violate_pattern(ds, self.hard_patterns, temp_learner.pta.G)
                    violate_soft_pattern, violated_soft_label = is_violate_pattern(ds, self.soft_patterns, temp_learner.pta.G)
                    if violate_hard_pattern:
                        ds.merging_score = -1
                        # write_to_file_in_new_line(self.with_pattern_file_name,
                        #                           f'Blocked => score: {ds.merging_score}')
                        self.merge_blocked_by_pattern += 1
                    elif violate_soft_pattern:
                        # bias_merging_score(ds, soft_pattern, temp_learner.pta.G)
                        decrease_score(ds, self.soft_patterns[violated_soft_label]['percentage_of_appearance'])
                        ds.biased_score = ds.merging_score + ds.biased_by
                        # write_to_file_in_new_line(self.with_pattern_file_name, f'= > bisaed_score: {ds.biased_score}')
                        self.merge_biased_by_pattern += 1
                    else:
                        ds.biased_score = ds.merging_score

                    if ds.biased_score > 0:
                        mergable_states.append(ds)
                        valid_for_at_least_one_red = True
                else:
                    ds.merging_score = -1
                    # write_to_file_in_new_line(self.with_pattern_file_name,
                    #                           f'Merging {ds.s1} & {ds.s2} => score: {ds.merging_score}')

            if not valid_for_at_least_one_red:
                # the blue_state can't be merged with any red_state
                self.make_it_red(blue)
                self.make_children_blue(blue)
                break

        if valid_for_at_least_one_red:
            ds_with_highest_scour = self.pick_high_biased_score_pair(mergable_states)
            # write_to_file_in_new_line(self.with_pattern_file_name, '*' * 30)
            # write_to_file_in_new_line(self.with_pattern_file_name,
            #                           f'{ds_with_highest_scour.s1} & {ds_with_highest_scour.s2} has the highest scour : {ds_with_highest_scour.biased_score}')

            if ds_with_highest_scour.s1.get_reference_state() != ds_with_highest_scour.s2.get_reference_state():
                # write_to_file_in_new_line(self.with_pattern_file_name,
                #                           f'Incorrect merge: {ds_with_highest_scour.s1} & {ds_with_highest_scour.s2}')
                self.incorrect_merge_counter += 1
            else:
                self.correct_merge_counter += 1
            # write_to_file_in_new_line(self.with_pattern_file_name, '*' * 30)
            self.merge_sets(ds_with_highest_scour)

        self.update_red_states()
        self.run_EDSM_with_pattern_learner_partial_merger()

    def make_it_red(self, blue_state):
        if blue_state in self.blue_states:
            self.blue_states.remove(blue_state)
            blue_state.color = 'red'
            self.red_states.append(blue_state)

    def make_children_blue(self, state):
        if isinstance(self.pta.G.graph[state], dict):
            children = self.pta.G.graph[state].keys()
            for child in children:
                if child.color != 'red':
                    child.color = 'blue'
    def update_blue_states(self):
        blue_states = []
        for red in self.red_states:
            children = self.pta.G.get_children(red)
            for child in children:
                if child.color != 'red':
                    child.color = 'blue'
                    blue_states.append(child)
        self.blue_states = blue_states


    def update_red_states(self):
        new_list = []
        for state in self.pta.G.get_all_states():
            if state.color == 'red':
                new_list.append(state)

        self.red_states = new_list

    def make_set_for_every_state_rooted_at(self, ds, s):
        ds.make_set(s)
        descendants = self.pta.G.get_descendants(s)
        for d in descendants:
            ds.make_set(d)


    def is_valid_merge(self, ds):
        all_sets = ds.get_sets()
        for representative, _set in all_sets.items():
            if len(_set) > 1:
                type_compatible, list_type = self.is_compatible_type(_set)
                input_compatible = self.is_input_compatible2(_set)
                if not type_compatible or not input_compatible:
                    return False
        return True

    def compute_score_accepted_states(self, ds):
        states_count_before_merge = 0
        all_sets = ds.get_sets()
        for representative, elements in all_sets.items():
            if representative.type == 'accepted':
                states_count_before_merge += len(elements)
        states_count_after_merge = len([state for state in all_sets.keys() if state.type == 'accepted'])
        merging_scour = states_count_before_merge - states_count_after_merge
        return merging_scour

    def try_to_merge_sets(self, ds):
        sets = ds.get_sets()
        for set in sets.items():
            representative, states = set
            if len(states) > 1:
                self.try_to_merge_states(representative, states)
                # check if the graph is disconnected after the merge
        # if self.pta.G.is_disconnected():
        #     print(f'Graph is disconnected after merging {ds.s1} with {ds.s2}')

    def try_to_merge_states(self, target, merge_list):
        # graph_before_merge = copy.deepcopy(self.pta.G)
        list_type = self.get_list_type(merge_list)
        target.type = list_type
        # if any (state.color == 'red' for state in merge_list):
        #     target.color = 'red'
        merge_list.remove(target)

        for i in range(0, len(merge_list)):
            source = merge_list[i]
            self.transfer_out_edge(source, target)
            self.transfer_in_coming_edges(source, target)

            # if source == self.pta.G.initial_state:
            #     self.pta.G.initial_state = target
            #     self.pta.G.initial_state.isInitial = True
            # if source != target:  # this if to solve butterfly problem
            #     self.pta.G.delete_state(source)


        #     compare the graph before and after the merge
        return target
    def merge_sets(self, ds):
        sets = ds.get_sets()
        for set in sets.items():
            representative, states = set
            if len(states)>1:
                self.merge_states(representative, states)
                # check if the graph is disconnected after the merge
        # if self.pta.G.is_disconnected():
        #     print(f'Graph is disconnected after merging {ds.s1} with {ds.s2}')

    def merge_states(self, target, merge_list):
        # graph_before_merge = copy.deepcopy(self.pta.G)
        list_type = self.get_list_type(merge_list)
        if any (state.color == 'red' for state in merge_list):
            target.color = 'red'
        merge_list.remove(target)

        for i in range(0, len(merge_list)):
            source = merge_list[i]
            self.transfer_out_edge(source, target)
            self.transfer_in_coming_edges(source, target)

            if source == self.pta.G.initial_state:
                self.pta.G.initial_state = target
                self.pta.G.initial_state.isInitial = True
            if source != target:  # this if to solve butterfly problem
                self.pta.G.delete_state(source)
                target.type = list_type

        #     compare the graph before and after the merge
        return target


    def mergre_rejected_states(self):
        rejected_states = []
        for state in self.pta.G.get_all_states():
            if state.type == 'rejected':
                rejected_states.append(state)
        target = rejected_states[0]
        self.merge_states(target, rejected_states)
        return target

    def transfer_out_edge(self, source, target):
        if source == target:
            return
        # mylist is temp list to make a copy of the out_edges list
        source_out_edges = self.pta.G.get_outgoing_transitions_for_state(source)

        for e in source_out_edges:
            target_out_edges = self.pta.G.get_outgoing_transitions_for_state(target)
            if self.is_in_target_out_edges(e, target_out_edges):
                continue

            # if the edge is a self loop in the source state move it to the target state
            if e.is_self_loop():
                self.pta.G.add_transition(target, target, e.input_key, e.output_key)
            else:
                self.pta.G.add_transition(target, e.to_state, e.input_key, e.output_key)

            self.pta.G.delete_Transition(e)

    def is_in_target_out_edges(self, edge_tuple, edges_list):
        for e in edges_list:
            # if both edges have the same label
            if e.input_key == edge_tuple.input_key and e.output_key == edge_tuple.output_key:
                return True
        return False


    def transfer_in_coming_edges(self, source, target):
        source_incoming_transitions = self.pta.G.get_incoming_transitions(source)

        for e in source_incoming_transitions:
            if not self.pta.G.has_incoming_transition_label(target, e):
                self.pta.G.add_transition(e.from_state, target, e.input_key, e.output_key)
            self.pta.G.delete_Transition(e)

    def is_input_compatible2(self, states_list):
        outgoing_transitions_list = self.pta.G.get_outgoing_transitions_for_list_of_states(None, states_list)
        input_dict = {}
        target_state_dict = {}
        for transition in outgoing_transitions_list:
            if transition.input_key not in input_dict:
                input_dict[transition.input_key] = set()
                target_state_dict[transition.input_key] = []
            if transition.to_state.type == 'accepted':
                input_dict[transition.input_key].add(transition.output_key)

        for input, output in input_dict.items():
            if len(output) > 1: # the same input will have more than one output
                return False
        return True

    # is_compatible_type: boolean
    # return true is s1 and s2 of the same type or at least of them is unlabeled
    # return false if one is rejected the other is accepted
    def is_compatible_type(self, list):
        compatible = False
        list_type = 'unlabeled'
        if any (state.type == 'rejected' for state in list):
            if any(state.type == 'accepted' for state in list):
                # some rejected and some accepted
                compatible = False
            else: # at least one is rejected and all other are unlabeled
                compatible = True
                list_type = 'rejected'
        elif any(state.type == 'accepted' for state in list):
            # some are accepted and non are rejected
            list_type = 'accepted'
            compatible = True
        else:
            # all unlabeled
            compatible = True
            list_type = 'unlabeled'

        return compatible, list_type

    def get_list_type(self, merge_list):
        _c, typ = self.is_compatible_type(merge_list)
        return typ

    def pick_high_biased_score_pair(self, list_of_mergable_states):# list of disjoint_sets object
        # Sort the list of lists based on the merging_scour (3rd item)
        list_of_mergable_states.sort(key=lambda x: x.biased_score, reverse=True)
        # pick up the pair with the highest scour
        ds_with_highest_scour = list_of_mergable_states.pop(0)
        return ds_with_highest_scour

    def compute_classes2(self,ds ,work_to_do):
        add_something_new = False
        go_agin = False
        updated_work_to_do= work_to_do.copy()
        for represitative, set_to_merge in work_to_do.items():
            checked_lables = []
            for s1 in set_to_merge:
                current_state_out_transitions = self.pta.G.get_outgoing_transitions_for_state(s1)
                other_state_out_transitions = self.pta.G.get_outgoing_transitions_for_list_of_states(s1, set_to_merge)
                for s1_trans in current_state_out_transitions:
                    label = s1_trans.label
                    if label not in checked_lables:
                        checked_lables.append(label)
                        for other_state_out_trans in other_state_out_transitions:
                            if label == other_state_out_trans.label:
                                s1_target_state = s1_trans.to_state
                                s2_target_state = other_state_out_trans.to_state
                                add_something_new = ds.union(s1_target_state, s2_target_state)
                                updated_work_to_do[ds.find(s1_target_state)] = ds.get_set(s1_target_state)
                                if add_something_new:
                                    go_agin = True
        if go_agin:
            self.compute_classes2(ds, updated_work_to_do)

    def write_statistics(self, file_name):
        write_to_file_in_new_line(file_name, f'Size of actual model(APTA): {self.sizeof_actual_system}')
        write_to_file_in_new_line(file_name, f'Correct merges: {self.correct_merge_counter}')
        write_to_file_in_new_line(file_name, f'Incorrect merges: {self.incorrect_merge_counter}')
        write_to_file_in_new_line(file_name, f'Size of learned model (baised_EDSM): {len(self.pta.G.get_all_states())}')
        write_to_file_in_new_line(file_name, f'number of hard patterns: {len(self.hard_patterns)}')
        write_to_file_in_new_line(file_name, f'number of blocked potential-merges by hard patterns: {self.merge_blocked_by_pattern}')
        write_to_file_in_new_line(file_name, f'number of soft patterns: {len(self.soft_patterns)}')
        write_to_file_in_new_line(file_name, f'number of biased potential-merges by soft patterns: {self.merge_biased_by_pattern}')