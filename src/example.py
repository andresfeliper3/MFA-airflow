from src.Biocode.managers.SequenceManager import SequenceManager
from src.Biocode.sequences.Sequence import Sequence

from src.Biocode.managers.GenomeManager import GenomeManager
from src.Biocode.managers.RegionGenomeManager import RegionGenomeManager
from src.Biocode.managers.RegionSequenceManager import RegionSequenceManager

from src.load import chromosome_I_c_elegans, c_elegans_data


#c_elegans_manager_cI = SequenceManager(sequence=Sequence(chromosome_I_c_elegans, name="chromosomeI"))
#c_elegans_manager_cI.calculate_and_graph()
#c_elegans_manager_cI.graph_cgr()

#c_elegans_manager = RegionGenomeManager(genome_data=c_elegans_data, organism_name="Caenorhabditis elegans", regions_number=3)
#c_elegans_manager.calculate_and_graph_only_merged()
#c_elegans_manager.graph_cgr()

c_elegans_manager = RegionSequenceManager(sequence_data=c_elegans_data[0], regions_number=3, sequence_name="Caenorhabditis elegans")
c_elegans_manager.calculate_and_graph()
c_elegans_manager.graph_cgr()

selected_columns = ["D-20", "D-2", "D-1", "D1", "D2", "D20", "DDq", "t(q=20)"]
#print(c_elegans_manager.generate_df_results(selected_columns))