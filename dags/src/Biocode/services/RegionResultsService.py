from AbstractService import AbstractService


class RegionResultsService(AbstractService):
    def __init__(self):
        self.table_name = "chr_region_results"
        self.columns = ["regions_number", "organism_id", "Dq_values", "tau_q_values", "DDq"]
        self.pk_column = "id"
