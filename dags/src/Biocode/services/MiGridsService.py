from AbstractService import AbstractService


class MiGridsService(AbstractService):
    def __init__(self):
        self.table_name = "mi_grids"
        self.columns = ["mi_grid", "organism_id", "epsilon_size"]
        self.pk_column = "id"