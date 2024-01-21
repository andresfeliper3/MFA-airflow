from src.Biocode.services.AbstractService import AbstractService


class WholeResultsService(AbstractService):
    def __init__(self):
        self.table_name = "chr_whole_results"
        self.columns = ["chromosome_id", "Dq_values", "tau_q_values", "DDq"]
        self.pk_column = "id"


