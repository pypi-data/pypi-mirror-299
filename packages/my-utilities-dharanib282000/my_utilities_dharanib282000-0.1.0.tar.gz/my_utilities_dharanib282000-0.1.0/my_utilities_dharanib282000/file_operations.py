import os

def read_file(file_path):
    """Read the contents of a file and return it as a string."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """Write the provided content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)
