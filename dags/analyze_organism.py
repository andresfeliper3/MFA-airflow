from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonVirtualenvOperator

def start_organism(organism_name):


def MFA(organism_name, chromosome):
    try:
        import os
        import sys
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from src.Biocode.managers.GenomeManager import GenomeManager
    except ImportError as e:
        print(f"Error importing necessary modules: {e}")
        raise
    c_elegans_manager = GenomeManager(genome_data=[chromosome], organism_name=organism_name)
    df = c_elegans_manager.save_to_db()
    #c_elegans_manager.calculate_multifractal_analysis_values()
    #df = c_elegans_manager.generate_df_results()
    print(df)
    #c_elegans_manager.calculate_and_graph_only_merged()
   # print(c_elegans_manager.get_mfa_results())

    print("SUCCESS")


with DAG("analyze_organism", description="MFA of organism",
         start_date=datetime(2024, 1, 15), schedule_interval="@once") as dag:
    """
    1. Read xlsx file and read organism info and GCF.
    2. Download the organism genome.
    3. Execute the MFA.
    4. Save the data in SQLite.
    4. Generate xslx and png from the db.
    """
    from src.load import c_elegans_data

    for i, chromosome_data in enumerate(c_elegans_data[:1]):
        task_id = f"MFA_{i}"
        t1 = PythonVirtualenvOperator(
            task_id=task_id,
            python_callable=MFA,
            op_args=["Caenorhabditis elegans", chromosome_data],
            requirements=[
                "biopython",
                "matplotlib",
                "xlsxwriter",
                "openpyxl"
                # Add other dependencies as needed
            ],
        )

        # Set task dependencies if needed

        if i > 0:
           t1.set_upstream(dag.get_task(f"MFA_{i - 1}"))
