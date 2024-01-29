from src.Biocode.managers.DBConnectionManager import DBConnectionManager
from src.Biocode.services.AbstractService import AbstractService


class WholeResultsService(AbstractService):
    def __init__(self):
        self.table_name = "chr_whole_results"
        self.columns = ["chromosome_id", "Dq_values", "tau_q_values", "DDq"]
        self.pk_column = "id"

    def extract_results(self):
        query = f"SELECT chr_whole_results.id as results_id, o.name as organism_name, chromosomes.id as chromosome_id \
                    , chromosomes.name as sequence_name, DDq, " \
                f"Dq_values, tau_q_values, cover, cover_percentage FROM chr_whole_results  JOIN chromosomes ON " \
                f"chr_whole_results.chromosome_id = chromosomes.id JOIN organisms o on chromosomes.organism_id = o.id;"
        return DBConnectionManager.extract_with_custom_query(query)
