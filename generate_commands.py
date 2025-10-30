import random

from write_clear_file import write_to_file_in_new_line, clear_file
#'TCP', coffeemachine','openSSL', 'bluetooth'
system_list = [ 'bluetooth']
file_name = f'commands_bletooth_15_RT.txt'
#'Run_classical_EDSM',
learning_strategy_list = [
                          'Run_classical_EDSM',
                          'Run_biased_EDSM',
                          'Run_biased_EDSM_sat',
                          'Run_biased_EDSM_satpat',
                          'Run_biasedSicco_EDSM_sat',
                          'Run_biasedSicco_EDSM_satpat',
                          'Run_DFASAT_sicco'
    ]
clear_file(file_name)

# [150, 300, 450, 600, 750, 900, 1050, 1200, 1350]
for system in system_list:
                        #500 750 1000 1250 1500 1750 2000 2250 2500 2750
    for walks_size in [1500, 2250, 3000, 3750, 4500, 5250, 6000, 6750, 7500, 8250]:
        for trail in range(10):
            seed = random.randint(1, 10000)
            for learning_strategy in learning_strategy_list:
                # command = f"python3 -m cProfile -o profiles/task_<jobid>_<arrayid>.prof -s time {learning_strategy}.py {seed} result {system} {trail} {walks_size}"
                #python3 -m cProfile -o profiles/task_<jobid>_<arrayid>.prof -s time Run_biased_EDSM.py 4419 result coffeemachine 0 500
                command = f"python3 {learning_strategy}.py {seed} result {system} {trail} {walks_size}"
                write_to_file_in_new_line(file_name, command)