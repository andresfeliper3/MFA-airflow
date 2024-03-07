import time
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Get the absolute path of the parent directory
sys.path.append(project_root) # Add the project root to the Python path

from src.Biocode.managers.GenomeManager import GenomeManager
from src.Biocode.managers.DBConnectionManager import DBConnectionManager
from src.load import data, ORGANISM_NAME, GCF, AMOUNT_CHROMOSOMES, REGIONS_NUMBER


start_time = time.time()
DBConnectionManager.start()
genome_manager = GenomeManager(genome_data=[data[0]], organism_name=ORGANISM_NAME)
genome_manager.calculate_multifractal_analysis_values()
genome_manager.save_to_db(GCF=GCF)
genome_manager.generate_df_results()

print(genome_manager.get_mfa_results())
DBConnectionManager.close()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"The process took {elapsed_time} seconds.")