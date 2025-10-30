import time

# from Learners.DFASAT.formula_builder import build_formula
from Learners.DFASAT.formula_builder_2410 import build_formula ,build_formula_with_patterns
from Learners.DFASAT.minisat import run_minisat
from Learners.DFASAT.variables_definer import set_variables
from Learners.DFASAT.visualizer import get_model, dict_to_graph
from write_clear_file import clear_file, write_to_file_in_new_line


class SAT:
    def __init__(self, graph):
        self.graph = graph
        self.num_of_colors = 2
        self.number_of_states = len(self.graph.get_all_states())
        self.sat_calls = 0
        self.total_sat_time = 0.0
        self.variables_map={}
        self.clauses_size=0
        self.sat_result = "UNSAT"
        self.model_graph_obj = None


    def run_dfasat(self, system_name): #, exploration_map
        # start_time = time.time()

        while self.sat_result == "UNSAT" and self.num_of_colors <= self.number_of_states:
            self.sat_calls += 1
            formula_file_path = f'{system_name}_formula.txt'
            clear_file(formula_file_path)

            self.variables_map = set_variables(self.num_of_colors, self.graph)
            # clear_file(f'{system_name}_dfasat_variables.txt')
            # for var_name, var_value in self.variables_map.items():
            #    write_to_file_in_new_line(f'{system_name}_dfasat_variables.txt', f"{var_name}: {var_value}")
            self.clauses_size = build_formula(self.num_of_colors, self.graph, formula_file_path, self.variables_map)
            #Running minisat
            self.sat_result = run_minisat(formula_file_path, system_name, len(self.variables_map), self.clauses_size)

            if self.sat_result == "UNSAT":
                # print ("UNSAT")
                self.num_of_colors += 1
            elif self.sat_result == "Unknown output format":
                # print("Unknown output format")
                break
            else:
                model_dict = get_model(self.sat_result, self.variables_map, self.graph.get_initial_state())
                self.model_graph_obj = dict_to_graph(model_dict, self.graph)
                self.sat_result = "SAT"
        # self.total_sat_time += time.time() - start_time
        return self.model_graph_obj

    def run_dfasat_with_patterns(self, system_name, patterns_map): #, exploration_map
        # start_time = time.time()

        while self.sat_result == "UNSAT" and self.num_of_colors <= self.number_of_states:
            self.sat_calls += 1
            formula_file_path = f'{system_name}_formula.txt'
            clear_file(formula_file_path)

            self.variables_map = set_variables(self.num_of_colors, self.graph)
            # clear_file(f'{system_name}_dfasat_variables.txt')
            # for var_name, var_value in self.variables_map.items():
            #    write_to_file_in_new_line(f'{system_name}_dfasat_variables.txt', f"{var_name}: {var_value}")
            self.clauses_size = build_formula_with_patterns(self.num_of_colors, self.graph, formula_file_path, self.variables_map, patterns_map)
            #Running minisat
            self.sat_result = run_minisat(formula_file_path, system_name, len(self.variables_map), self.clauses_size)

            if self.sat_result == "UNSAT":
                # print ("UNSAT")
                self.num_of_colors += 1
            elif self.sat_result == "Unknown output format":
                # print("Unknown output format")
                break
            else:
                model_dict = get_model(self.sat_result, self.variables_map, self.graph.get_initial_state())
                self.model_graph_obj = dict_to_graph(model_dict, self.graph)#, sat_result
                self.sat_result = "SAT"
        # self.total_sat_time += time.time() - start_time
        return self.model_graph_obj

    def write_dfasat_report(self, file_path):
        with open(file_path, 'a') as f:
            f.write(f'\nDFASAT Statistics:\n')
            f.write(f'Number of colors used (automata_size): {self.num_of_colors}\n')
            f.write(f'Number of SAT solver calls: {self.sat_calls}\n')
            f.write(f'Number of variables in the last SAT call: {len(self.variables_map)}\n')
            f.write(f'Number of clauses in the last SAT call: {self.clauses_size}\n')
            f.write(f'SAT result: {self.sat_result}\n')
            # f.write(f'Total time spent in SAT solver (seconds): {self.total_sat_time:.4f}\n')

    # def get_number_of_colors(red_states):
    #     number_of_colors = 0
    #     for state in red_states:
    #         if state.type == 'accepted':
    #             number_of_colors +=1
    #     # add a color for the rejected state
    #     number_of_colors += 1  # for the rejected state
    #     return number_of_colors