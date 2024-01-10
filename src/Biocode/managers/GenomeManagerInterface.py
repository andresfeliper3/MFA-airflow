import pandas as pd
import os

from src.Biocode.sequences.Genome import Genome
from src.Biocode.sequences.Sequence import Sequence
from src.Biocode.managers.SequenceManager import SequenceManager

PATH = "Biocode/out/results"


class GenomeManagerInterface:

    def __init__(self, genome: Genome = None, genome_data: list[dict] = None, chromosomes: list[Sequence] = None,
                 organism_name: str = None,
                 regions_number: int = 0):

        self.df_results = None
        self.regions_number = regions_number
        if genome:
            self.genome = genome
        elif genome_data:
            self.genome = Genome(chromosomes_data=genome_data, regions_number=regions_number)
        elif chromosomes:
            self.genome = Genome(chromosomes=chromosomes, regions_number=regions_number)

        # Managers
        self.managers = []
        if regions_number < 0:
            raise Exception("Not a valid regions_number for the GenomeManager constructor")
        elif regions_number == 0:
            for chromosome in self.genome.get_chromosomes():
                self.managers.append(SequenceManager(sequence=chromosome, sequence_name=chromosome.get_name()))
        else:  # > 0
            for chromosome in self.genome.get_chromosomes():
                self.managers.append(RegionSequenceManager(sequence=chromosome, sequence_name=chromosome.get_name(),
                                                           regions_number=regions_number))
            # regions names
            self.regions_names = []
            self._attach_regions_names()

        # name of organism
        self.organism_name = organism_name
        # mfa results
        self.mfa_results = []
        # degrees of multifractality
        self.degrees_of_multifractality = []
        # coverage
        self.cover_percentage = []
        self.cover = []

    def graph_3d_cgr(self, all=True, index=0, grid_size=512):
        """Graph CGR density in a 3D chart"""
        if not all:
            self.managers[index].graph_3d_cgr(grid_size)
        else:
            for manager in self.managers:
                manager.graph_3d_cgr(grid_size)

    def graph_linear_fit(self):
        """Graph linear fit for fq vs ln(epsilon)"""
        for manager in self.managers:
            manager.graph_linear_fit()

    def generate_degrees_of_multifractality(self):
        """Generate degrees of multifractality"""
        pass

    def graph_multifractal_spectrum(self):
        """Graph multifractal spectrum of Dq vs q"""
        pass

    def graph_correlation_exponent(self):
        """Graph t(q) vs q"""
        pass

    def calculate_multifractal_analysis_values(self):
        """Generate mfa generators, generate mfa values, attach the degrees of multifractality, the cover and cover 
        percentage"""
        for manager in self.managers:
            manager.calculate_multifractal_analysis_values()
            self.cover.append(manager.get_cover())
            self.cover_percentage.append(manager.get_cover_percentage())
            self.mfa_results.append(manager.get_mfa_results())

        self.generate_degrees_of_multifractality()

    def graph_multifractal_analysis(self, _3d_cgr=True, degrees_of_multifractality=True,
                                    multifractal_spectrum=True, correlation_exponent=True, top_labels=True):
        """Graph the multifractal analysis values using the chart of 3D density of points, the linear fit fq vs q, 
        the multifractal spectrum Dq vs q, and the correlation exponent t(q) vs q"""
        for manager in self.managers:
            manager.graph_multifractal_analysis(_3d_cgr, degrees_of_multifractality, multifractal_spectrum,
                                                correlation_exponent, top_labels=top_labels)

    def graph_multifractal_analysis_merged(self):
        """Graph mutifractal analysis charts with merged values"""
        pass

    def graph_coverage(self):
        """Graph the barplot representing the coverage of the DNA sequence (the nucleotides that have been 
        identified)"""
        for manager in self.managers:
            manager.graph_coverage()

    def calculate_and_graph(self):
        """Generate MFA values and graph them along with the coverage"""
        pass

    def generate_df_results(self, mfa_results, row_labels, q_min, q_max, selected_columns: list = None, ):
        # Create an empty DataFrame with the correct number of rows
        self.df_results = pd.DataFrame(index=row_labels, columns=["D%d" % i for i in range(q_min, q_max + 1)])

        # Code to populate the DataFrame
        for i, data_dict in enumerate(mfa_results):
            self.df_results.loc[row_labels[i]] = data_dict['Dq_values']

        self.df_results['DDq'] = [data_dict['DDq'] for data_dict in mfa_results]
        self.df_results['t(q=20)'] = [data_dict['tau_q_values'][-1] for data_dict in mfa_results]

        selected_df_results = self.df_results[selected_columns] if selected_columns else self.df_results
        self._save_df_results(selected_df_results)
        return selected_df_results

    def _save_df_results(self, df):
        os.makedirs(PATH, exist_ok=True)

        # Guardar el DataFrame en un archivo Excel
        output_file = f'{PATH}/{self.organism_name}.xlsx'
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
