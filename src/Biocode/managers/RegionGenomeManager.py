from src.Biocode.managers.GenomeManagerInterface import GenomeManagerInterface
from src.Biocode.sequences.Genome import Genome

from src.Biocode.sequences.Sequence import Sequence
from src.Biocode.graphs.Graphs import Graphs


class RegionGenomeManager(GenomeManagerInterface):
    def __init__(self, genome: Genome = None, genome_data: list[dict] = None, chromosomes: list[Sequence] = None,
                 organism_name: str = None,
                 regions_number: int = 0):
        super().__init__(genome, genome_data, chromosomes, organism_name, regions_number)

    def _attach_regions_names(self):
        for manager in self.managers:
            self.regions_names += manager.get_regions_names()

    def generate_degrees_of_multifractality(self):
        for manager in self.managers:
            if len(manager.get_degree_of_multifractality()) == 0:
                manager.generate_degree_of_multifractality()
            self.degrees_of_multifractality += manager.get_degree_of_multifractality()

    def graph_degrees_of_multifractality(self, y_range=None, legend_labels=None,
                                         top_labels=False):
        # Check if the lengths of x_array and y_array match

        if legend_labels is None:
            legend_labels = ['Left', 'Center', 'Right']
        if len(self.regions_names) != len(self.degrees_of_multifractality):
            raise ValueError(
                f"Number of chromosome names {len(self.genome.get_chromosomes_names())} ({self.genome.get_chromosomes_names()}) \
        does not match the number of y_array {len(self.degrees_of_multifractality)} ({self.degrees_of_multifractality}).")

        Graphs.graph_bars_grouped(x_array=self.regions_names, y_array=self.degrees_of_multifractality,
                                  title=f"Degrees of multifractality by regions of {self.organism_name}",
                                  y_label="Degrees of multifractality",
                                  x_labels=self.genome.get_chromosomes_names(), legend_labels=legend_labels,
                                  regions_number=self.regions_number,
                                  y_range=y_range, top_labels=top_labels)

    def graph_multifractal_spectrum(self, color_by='region'):
        Graphs.graph_many_grouped(results_array=self.flattened_mfa_results, X='q_values', Y='Dq_values', x_label='q',
                                  y_label='Dq',
                                  title=f"Multifractal spectrum of genome by regions of {self.organism_name}",
                                  regions_number=self.regions_number, labels_array=self.regions_names,
                                  color_by=color_by)

    def graph_correlation_exponent(self, color_by='region', markersize=3):
        Graphs.graph_many_grouped(results_array=self.flattened_mfa_results, X='q_values', Y='tau_q_values', x_label='q',
                                  y_label='t(q)',
                                  title=f"Correlation exponent of genome by regions of {self.organism_name}",
                                  regions_number=self.regions_number, labels_array=self.regions_names,
                                  color_by=color_by, markersize=markersize)

    def calculate_multifractal_analysis_values(self):
        super().calculate_multifractal_analysis_values()
        self._generate_flattened_mfa_results_and_cover()

    def _generate_flattened_mfa_results_and_cover(self):
        self.flattened_mfa_results = [region for chromosome in self.mfa_results for region in chromosome]
        self.cover_percentage = [region for chromosome in self.cover_percentage for region in chromosome]
        self.cover = [region for chromosome in self.cover for region in chromosome]

    def graph_multifractal_analysis_merged(self, y_range_degrees_of_multifractality=None,
                                           degrees_of_multifractality=True,
                                           multifractal_spectrum=True, correlation_exponent=True,
                                           regions_labels=['Left', 'Center', 'Right'],
                                           color_by='region', top_labels=False):
        if degrees_of_multifractality:
            self.graph_degrees_of_multifractality(y_range=y_range_degrees_of_multifractality,
                                                  legend_labels=regions_labels,
                                                  top_labels=top_labels)
        if multifractal_spectrum:
            self.graph_multifractal_spectrum(color_by=color_by)
        if correlation_exponent:
            self.graph_correlation_exponent(color_by=color_by, markersize=3)

    def calculate_and_graph(self, y_range_degrees_of_multifractality=None, _3d_cgr=True,
                            degrees_of_multifractality=True,
                            multifractal_spectrum=True, correlation_exponent=True, top_labels=False):
        self.calculate_multifractal_analysis_values()
        self.graph_multifractal_analysis(y_range_degrees_of_multifractality, _3d_cgr, degrees_of_multifractality,
                                         multifractal_spectrum,
                                         correlation_exponent, top_labels)

    def calculate_and_graph_plus_merged(self, y_range_degrees_of_multifractality=None, _3d_cgr=True,
                                        degrees_of_multifractality=True,
                                        multifractal_spectrum=True, correlation_exponent=True, top_labels=False,
                                        regions_labels=['Left', 'Center', 'Right'], color_by='region'):
        self.calculate_multifractal_analysis_values()
        self.graph_multifractal_analysis(y_range_degrees_of_multifractality, _3d_cgr, degrees_of_multifractality,
                                         multifractal_spectrum,
                                         correlation_exponent, top_labels)
        self.graph_multifractal_analysis_merged(y_range_degrees_of_multifractality, degrees_of_multifractality,
                                                multifractal_spectrum,
                                                correlation_exponent, regions_labels, color_by, top_labels)

    def calculate_and_graph_only_merged(self, y_range_degrees_of_multifractality=None, degrees_of_multifractality=True,
                                        multifractal_spectrum=True, correlation_exponent=True, top_labels=False,
                                        regions_labels=['Left', 'Center', 'Right'], color_by='region'):
        self.calculate_multifractal_analysis_values()
        self.graph_multifractal_analysis_merged(y_range_degrees_of_multifractality, degrees_of_multifractality,
                                                multifractal_spectrum,
                                                correlation_exponent, regions_labels, color_by, top_labels)

    def generate_df_results(self, selected_columns: list = None):
        # Extract sequence names and use them as row labels
        row_labels = self.regions_names
        # Extract sequence names and use them as row labels
        q_min = self.managers[0].get_managers()[0].get_mfa_generator().get_q_min()
        q_max = self.managers[0].get_managers()[0].get_mfa_generator().get_q_max()
        return super().generate_df_results(self.flattened_mfa_results, row_labels, q_min, q_max, selected_columns)

    def set_organism_name(self, organism_name):
        self.organism_name = organism_name

    def get_organism_name(self):
        return self.organism_name

    def get_genome(self):
        return self.genome

    def get_mi_grids(self):
        return self.mi_grids

    def get_mfa_results(self):
        return self.mfa_results

    def get_degrees_of_multifractality(self):
        return self.degrees_of_multifractality

    def get_managers(self) -> list:
        return self.managers

    def get_regions_names(self) -> list[str]:
        return self.regions_names

    def get_cover(self) -> list[list[int]]:
        return self.cover

    def get_cover_percentage(self) -> list[float]:
        return self.cover_percentage
