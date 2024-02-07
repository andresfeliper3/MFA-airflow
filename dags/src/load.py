import os
import yaml

# Load configurations from the YAML file

sequences_file_path = os.path.join(os.path.dirname(__file__), 'sequences.yaml')
with open(sequences_file_path, 'r') as sequences_file:
    config = yaml.safe_load(sequences_file)

sequences_folder = os.path.join(os.path.dirname(__file__), config["sequences_folder"])


# Function to read fasta sequence
def read_fasta_sequence(file_path):
    sequence = ""

    with open(file_path, "r") as file:
        lines = file.readlines()

        # Skip header lines (lines starting with '>')
        sequence_lines = [line.strip() for line in lines if not line.startswith(">")]

        # Concatenate the lines to form the sequence
        sequence = "".join(sequence_lines)

    return sequence


ORGANISM_NAME = config['organism_name']
GCF = config['GCF']
AMOUNT_CHROMOSOMES = config['amount_chromosomes']
REGIONS_NUMBER = config['regions_number']
ORGANISM_FOLDER = config['organism_folder']

organism_path = os.path.abspath(os.path.join(sequences_folder, ORGANISM_FOLDER))


def create_sequence_data_dict(path):
    files = os.listdir(path)
    return [
        {"path": os.path.join(path, file), "name": file.split(".")[0]}
        for file in files
    ]


data = create_sequence_data_dict(organism_path)
