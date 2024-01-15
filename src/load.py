from Bio import SeqIO
import os
import yaml


def process_sequence_data(sequences_folder, subfolder, data):
    return [
        {"path": os.path.abspath(os.path.join(sequences_folder, subfolder, entry["path"])), "name": entry["name"]}
        for entry in data
    ]


# Load configurations from the YAML file
with open("sequences.yaml", "r") as sequences_file:
    config = yaml.safe_load(sequences_file)

sequences_folder = config["sequences_folder"]
c_elegans_data = process_sequence_data(sequences_folder, "c_elegans", config["c_elegans_data"])
musa_acuminata_data = process_sequence_data(sequences_folder, "musa_acuminata", config["musa_acuminata_data"])


# Function to read fasta sequence
def read_fasta_sequence(file_path):
    return str(SeqIO.read(file_path, "fasta").seq)


# Example usage
fasta_path_c_elegans_cI = c_elegans_data[0]["path"]
chromosome_I_c_elegans = read_fasta_sequence(fasta_path_c_elegans_cI)

fasta_path_musa_cI = musa_acuminata_data[0]["path"]
chromosome_I_musa = read_fasta_sequence(fasta_path_musa_cI)
