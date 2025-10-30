'''
The difference between 'w' (write) and 'a' (append) modes in file handling is as follows:
'w' mode:
    Opens the file for writing.
    If the file already exists, it overwrites the file, effectively clearing its contents.
    If the file does not exist, it creates a new file.
    Example use case: Writing new content to a file, replacing any existing content.
'a' mode:
    Opens the file for appending.
    If the file already exists, it preserves the existing content and appends new content to the end of the file.
    If the file does not exist, it creates a new file.
    Example use case: Adding new content to a file without removing the existing content.
'''
def write_to_file_in_new_line(filename, content):
    # Open the file in write mode ('w') or append mode ('a')
    with open(filename, 'a') as file:  # 'a' for append mode
        file.write(content)
        file.write('\n')  # Add a new line if needed

def write_to_file_in_line(filename, content):
    # Open the file in write mode ('w') or append mode ('a')
    with open(filename, 'a') as file:  # 'a' for append mode
        file.write(content)

def clear_file(filename):
    with open(filename, 'w'):
        pass  # Opening in 'w' mode truncates the file, clearing its contents.
