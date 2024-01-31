from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
import os

# Get the path to the directory of the current script
current_script_directory = os.path.dirname(os.path.abspath(__file__))
DAGS_FOLDER = os.path.join(current_script_directory)  # Assuming the DAGs folder is in the same directory

with DAG("download_organism", description="Download organism genome from the NCBI",
         start_date=datetime(2024, 1, 15), schedule_interval="@once") as dag:
    """
    # Setting the working directory to the DAGs folder
    os.chdir(DAGS_FOLDER)

    # Importing modules
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(current_script_directory, '..')))
    """

    SUBFOLDER = 'src/Biocode/dna_sequences/test'
    # Download command
    command = f'wget --recursive -e robots=off --reject "index.html" --no-host-directories --cut-dirs=6 https://ftp.ncbi.nlm.nih.gov/genomes/refseq/invertebrate/Caenorhabditis_elegans/latest_assembly_versions/GCF_000002985.6_WBcel235/ -P {current_script_directory}/{SUBFOLDER}'

    # BashOperator task
    t1 = BashOperator(
        task_id='download_org',
        bash_command=command
    )

    t1

    # Download with wget (checked)
    # Select the .gz that ends in _genomic.nfa
    # Unzip it
    # Read the file and separate it in chromosomes in a different folder

