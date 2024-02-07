from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator

import gzip
from shutil import unpack_archive
import os
import subprocess

# Get the path to the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))
ORGANISM_FOLDER = "Caenorhabditis_elegans"

SUBFOLDER = f'src/Biocode/dna_sequences/{ORGANISM_FOLDER}'


def clean_directory(**kwargs):
    directory = os.path.join(current_script_directory, SUBFOLDER)

    # List files in the directory
    files = os.listdir(directory)

    # Keep only files ending with ".gz" and delete others
    for file in files:
        file_path = os.path.join(directory, file)
        if not file.endswith(".gz"):
            os.remove(file_path)


def uncompress_all_files(**kwargs):
    directory = os.path.join(current_script_directory, SUBFOLDER)
    files = os.listdir(directory)

    for file in files:
        if file.endswith(".gz"):
            input_path = os.path.join(directory, file)
            output_path = os.path.join(directory, file.replace(".gz", ""))

            with gzip.open(input_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
                f_out.write(f_in.read())

            # Optionally, you can delete the compressed file if needed
            os.remove(input_path)
            print(f"Uncompressed file: {output_path}")


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


with DAG("download_organism", description="Download organism genome from the NCBI",
         start_date=datetime(2024, 1, 15), schedule_interval="@once") as dag:
    files_url = 'https://ftp.ncbi.nlm.nih.gov/genomes/refseq/invertebrate/Caenorhabditis_elegans/latest_assembly_versions/GCF_000002985.6_WBcel235/GCF_000002985.6_WBcel235_assembly_structure/Primary_Assembly/assembled_chromosomes/FASTA/'

    # Download command
    download_command = f'wget --recursive -np -e robots=off --reject "index.html" --no-host-directories --cut-dirs=10 {files_url} -P {current_script_directory}/{SUBFOLDER}'

    # BashOperator task to download genome
    t_download = BashOperator(
        task_id='download_genome',
        bash_command=download_command
    )

    t_clean = PythonOperator(
        task_id='clean_directory',
        python_callable=clean_directory,
        provide_context=True  # Provide context to access XCom values
    )

    # PythonOperator task to list and uncompress
    t_uncompress = PythonOperator(
        task_id='uncompress',
        python_callable=uncompress_all_files,
        provide_context=True  # Provide context to access XCom values
    )

    # Set task dependencies
    t_download >> t_clean >> t_uncompress


    # Read the chromosomes and use YAML (in progress) - check ORGANISM_FOLDER

