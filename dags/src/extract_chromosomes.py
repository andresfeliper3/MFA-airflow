from Bio import SeqIO


def extract_all_chromosomes(fasta_file):
    """
    Extract all chromosomes from a genome FASTA file.

    Parameters:
    - fasta_file: The path to the genome FASTA file.

    Returns:
    - A dictionary of SeqRecord objects with chromosome names as keys.
    """
    # Read the FASTA file
    records = SeqIO.to_dict(SeqIO.parse(fasta_file, "fasta"))

    return records


# Example usage
fasta_file_path = "Biocode/dna_sequences/test/GCF_000002985.6_WBcel235_cds_from_genomic.fna"

# Extract all chromosomes
all_chromosomes = extract_all_chromosomes(fasta_file_path)

# Print information about each chromosome
for chromosome_name, chromosome_record in all_chromosomes.items():
    print(f"Chromosome Name: {chromosome_name}")
    # print(f"Chromosome Sequence: {chromosome_record.seq}")
    print()
