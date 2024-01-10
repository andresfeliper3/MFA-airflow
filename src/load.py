from Bio import SeqIO
import os

# Define the main folder containing the sequences
sequences_folder = "Biocode/dna_sequences"

c_elegans_data = [
    {"path": os.path.abspath(os.path.join(sequences_folder, "c_elegans", "c_elegans_chromosome_I.fasta")), "name": "chromosome_I"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "c_elegans", "c_elegans_chromosome_II.fasta")), "name": "chromosome_II"},
    # Add more entries as needed
]

musa_acuminata_data = [
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_I.fasta")), "name": "chromosome_I"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_II.fasta")), "name": "chromosome_II"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_III.fasta")), "name": "chromosome_III"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_IV.fasta")), "name": "chromosome_IV"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_V.fasta")), "name": "chromosome_V"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_VI.fasta")), "name": "chromosome_VI"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_VII.fasta")), "name": "chromosome_VII"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_VIII.fasta")), "name": "chromosome_VIII"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_IX.fasta")), "name": "chromosome_IX"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_X.fasta")), "name": "chromosome_X"},
    {"path": os.path.abspath(os.path.join(sequences_folder, "musa_acuminata", "musa_acuminata_chromosome_XI.fasta")), "name": "chromosome_XI"},
]

# Function to read fasta sequence
def read_fasta_sequence(file_path):
    return str(SeqIO.read(file_path, "fasta").seq)

# Example usage
fasta_path_c_elegans_cI = c_elegans_data[0]["path"]
chromosome_I_c_elegans = read_fasta_sequence(fasta_path_c_elegans_cI)

fasta_path_musa_cI = musa_acuminata_data[0]["path"]
chromosome_I_musa = read_fasta_sequence(fasta_path_musa_cI)


