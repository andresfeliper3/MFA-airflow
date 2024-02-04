import os
import yaml


def process_sequence_data(sequences_folder, subfolder, data):
    return [
        {"path": os.path.abspath(os.path.join(sequences_folder, subfolder, entry["path"])), "name": entry["name"]}
        for entry in data
    ]


# Load configurations from the YAML file

sequences_file_path = os.path.join(os.path.dirname(__file__), 'sequences.yaml')
with open(sequences_file_path, 'r') as sequences_file:
    config = yaml.safe_load(sequences_file)

sequences_folder = os.path.join(os.path.dirname(__file__), config["sequences_folder"])
c_elegans_data = process_sequence_data(sequences_folder, "c_elegans", config["c_elegans_data"])
musa_acuminata_data = process_sequence_data(sequences_folder, "musa_acuminata", config["musa_acuminata_data"])


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


# Example usage
fasta_path_c_elegans_cI = c_elegans_data[0]["path"]
chromosome_I_c_elegans = read_fasta_sequence(fasta_path_c_elegans_cI)

fasta_path_musa_cI = musa_acuminata_data[0]["path"]
chromosome_I_musa = read_fasta_sequence(fasta_path_musa_cI)

# NEW VERSION
ORGANISM_NAME = config['organism_name']
GCF = config['GCF']
AMOUNT_CHROMOSOMES = config['amount_chromosomes']
REGIONS_NUMBER = config['regions_number']
ORGANISM_FOLDER = config['organism_folder']

organism_path = os.path.abspath(os.path.join(sequences_folder, ORGANISM_FOLDER))


def create_sequence_data_dict(path):
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
    return [
        {"path": file_path, "name": file.split(".")[0]}
        for file in files
    ]


data = create_sequence_data_dict(organism_path)
print(data)
