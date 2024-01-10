from src.Biocode.managers.SequenceManager import SequenceManager
from src.Biocode.sequences.Sequence import Sequence

from src.Biocode.managers.GenomeManager import GenomeManager

from src.load import chromosome_I_c_elegans, c_elegans_data

#chromosome_I_manager = SequenceManager(sequence=Sequence(sequence=chromosome_I_c_elegans), sequence_name='chromosome_I')
# chromosome_I_manager.calculate_and_graph()

c_elegans_manager = GenomeManager(genome_data=c_elegans_data, organism_name="Caenorhabditis elegans")

c_elegans_manager.calculate_and_graph_only_merged()

selected_columns = ["D-20", "D-2", "D-1", "D1", "D2", "D20", "DDq", "t(q=20)"]
print(c_elegans_manager.generate_df_results(selected_columns))