import csv
import os

from write_clear_file import clear_file


def get_time_EDSM(Input_filename, output_filename, column_name):
    with open(Input_filename, 'r') as file:
        finish_time = None
        for line in file:
            if 'Total time spent in EDSM (seconds): ' in line:
                finish_time = line.split('Total time spent in EDSM (seconds): ')[1].strip()
                break

        if finish_time is not None:
            write_header = not os.path.exists(output_filename)
            with open(output_filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if write_header:
                    writer.writerow([column_name])
                writer.writerow([finish_time])

def convert_all_statistics_to_csv_BiasedEDSM(directory, output_csv):
    header = [
        'file', 'Trails', 'Number of walks', 'Size of reference graph',
        'Alphabet_size', 'Size of actual model(APTA)', 'Correct merges',
        'Incorrect merges', 'Size of learned model (baised_EDSM)', 'number of hard patterns',
        'number of blocked potential-merges by hard patterns','number of soft patterns',
        'number of biased potential-merges by soft patterns','Total time spent in EDSM (seconds)',
        'number of Positive traces', 'number of Negative traces', 'True Positive', 'True Negative',
        'False Positive', 'False Negative', 'Precision', 'Recall', 'Specificity',
        'F-measure', 'Accuracy', 'BCR', 'Structural Difference'
    ]
    write_header = not os.path.exists(output_csv) or os.path.getsize(output_csv) == 0
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(header)
        for filename in os.listdir(directory):
            if filename.endswith('_statistics.txt'):
                filepath = os.path.join(directory, filename)
                values = {key: None for key in header}
                with open(filepath, 'r') as file:
                    for line in file:
                        for key in header:
                            if key + ':' in line:
                                values[key] = line.split(key + ':')[1].strip()
                values['file'] = filename.replace('_BaisedEDSM_statistics.txt', '')
                writer.writerow([values[key] for key in header])

def convert_all_statistics_to_csv_BiasedSAT(directory, output_csv):
    header = [
        'file', 'Trails', 'Number of walks', 'Size of reference graph',
        'Alphabet_size', 'Size of actual model(APTA)', 'Correct merges',
        'Incorrect merges', 'Size of learned model (baised_EDSM)', 'number of hard patterns',
        'number of blocked potential-merges by hard patterns','number of soft patterns',
        'number of biased potential-merges by soft patterns','Total time spent in EDSM (seconds)',
        'Number of colors used (automata_size)',
        'Number of SAT solver calls',
        'Number of variables in the last SAT call',
        'Number of clauses in the last SAT call',
        'SAT result',
        'Total time spent in SAT solver (seconds)',
        'number of Positive traces', 'number of Negative traces', 'True Positive', 'True Negative',
        'False Positive', 'False Negative', 'Precision', 'Recall', 'Specificity',
        'F-measure', 'Accuracy', 'BCR', 'Structural Difference'
    ]
    write_header = not os.path.exists(output_csv) or os.path.getsize(output_csv) == 0
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(header)
        for filename in os.listdir(directory):
            if filename.endswith('_statistics.txt'):
                filepath = os.path.join(directory, filename)
                values = {key: None for key in header}
                with open(filepath, 'r') as file:
                    for line in file:
                        for key in header:
                            if key + ':' in line:
                                values[key] = line.split(key + ':')[1].strip()
                values['file'] = filename.replace('_BiasedSAT_statistics.txt', '')
                writer.writerow([values[key] for key in header])

def convert_all_statistics_to_csv_DFASAT(directory, output_csv):
    header = [
        'file', 'Trails', 'Number of walks', 'Size of reference graph',
        'Alphabet_size', 'Size of actual model(APTA)', 'Correct merges',
        'Incorrect merges', 'Size of learned model(sicco_EDSM)','Total time spent in EDSM (seconds)',
        'Number of colors used(automata_size)',
        'Number of SAT solver calls',
        'Number of variables in the last SAT call',
        'Number of clauses in the last SAT call',
        'SAT result',
        'Total time spent in SAT solver(seconds)',
        'number of Positive traces', 'number of Negative traces', 'True Positive', 'True Negative',
        'False Positive', 'False Negative', 'Precision', 'Recall', 'Specificity',
        'F-measure', 'Accuracy', 'BCR', 'Structural Difference'
    ]
    write_header = not os.path.exists(output_csv) or os.path.getsize(output_csv) == 0
    with open(output_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow(header)
        for filename in os.listdir(directory):
            if filename.endswith('_statistics.txt'):
                filepath = os.path.join(directory, filename)
                values = {key: None for key in header}
                with open(filepath, 'r') as file:
                    for line in file:
                        for key in header:
                            if key + ':' in line:
                                values[key] = line.split(key + ':')[1].strip()
                values['file'] = filename.replace('_DFASAT_statistics.txt', '')
                writer.writerow([values[key] for key in header])
def split_csv_by_system(input_csv):
    import csv
    import os

    with open(input_csv, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        rows_by_system = {}

        for row in reader:
            systemname = row[0]
            parts = systemname.split('_')
            if len(parts) >= 3:
                key = f"{parts[0]}_{parts[2]}"
                if key not in rows_by_system:
                    rows_by_system[key] = []
                rows_by_system[key].append(row)

        for key, rows in rows_by_system.items():
            out_filename = f"statistics/{system_name}/{key}.csv"
            with open(out_filename, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                writer.writerows(rows)


if __name__ == "__main__":
    # system_name= "DFASAT"
    # clear_file(f'all_statistics_{system_name}.csv')
    # convert_all_statistics_to_csv_BiasedSAT(f'result/{system_name}', f'all_statistics_{system_name}.csv')
    # split_csv_by_system(f'all_statistics_{system_name}.csv')

    # system_name = "BiasedEDSM"
    # clear_file(f'all_statistics_{system_name}.csv')
    # convert_all_statistics_to_csv_BiasedEDSM(f'result/{system_name}', f'all_statistics_{system_name}.csv')
    # split_csv_by_system(f'all_statistics_{system_name}.csv')

    # system_name = "BiasedSAT"
    # clear_file(f'all_statistics_{system_name}.csv')
    # convert_all_statistics_to_csv_BiasedSAT(f'result/{system_name}', f'all_statistics_{system_name}.csv')
    # split_csv_by_system(f'all_statistics_{system_name}.csv')

    system_name = "BiasedSiccoSAT"
    clear_file(f'all_statistics_{system_name}.csv')
    convert_all_statistics_to_csv_BiasedSAT(f'result/{system_name}', f'all_statistics_{system_name}.csv')
    split_csv_by_system(f'all_statistics_{system_name}.csv')