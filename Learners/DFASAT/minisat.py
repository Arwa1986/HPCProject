import subprocess
from write_clear_file import write_to_file_in_new_line


def run_minisat(input_cnf, system_name, variables_size, clauses_size):
    output_file = f'{system_name}_SAT_result.txt'
    write_to_file_in_new_line(input_cnf, 'p cnf ' + str(variables_size) + ' ' + str(clauses_size))

    result = subprocess.run(['minisat', input_cnf, output_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    with open(output_file, 'r') as f:
        lines = f.readlines()

    if not lines:
        return "Unknown error or empty result"

    if lines[0].strip() == "UNSAT":
        return "UNSAT"
    elif lines[0].strip() == "SAT":
        model = list(map(int, lines[1].split()))
        # Filter out the zero at the end
        model = [v for v in model if v != 0]
        return model
    else:
        return "Unknown output format"