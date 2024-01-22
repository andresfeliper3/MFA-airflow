from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator


def _set_path():
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def load_organism(organism_name, gcf, amount_chromosomes):
    _set_path()
    from src.Biocode.managers.DBConnectionManager import DBConnectionManager
    from src.Biocode.services.OrganismsService import OrganismsService

    DBConnectionManager.start()
    organism_service = OrganismsService()
    organism_service.insert(record=(organism_name, gcf, amount_chromosomes))
    DBConnectionManager.close()


def MFA(organism_name, gcf, chromosome):

    try:
        import os
        import sys
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from src.Biocode.managers.GenomeManager import GenomeManager
        from src.Biocode.managers.DBConnectionManager import DBConnectionManager
    except ImportError as e:
        print(f"Error importing necessary modules: {e}")
        raise
    DBConnectionManager.start()
    c_elegans_manager = GenomeManager(genome_data=[chromosome], organism_name=organism_name)
    c_elegans_manager.calculate_multifractal_analysis_values()
    c_elegans_manager.save_to_db(GCF=gcf)
    c_elegans_manager.generate_df_results()

    # c_elegans_manager.calculate_and_graph_only_merged()
    print(c_elegans_manager.get_mfa_results())
    print("SUCCESS")
    DBConnectionManager.close()


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

    ORGANISM_NAME = "Caenorhabditis elegans"
    GCF = "GCF_000002985.6"
    AMOUNT_CHROMOSOMES = 6

    t1 = PythonOperator(task_id="load_org",
                        python_callable=load_organism,
                        op_args=[ORGANISM_NAME, GCF, AMOUNT_CHROMOSOMES])

    for i, chromosome_data in enumerate(c_elegans_data):
        task_id = f"MFA_{i+1}"
        task = PythonVirtualenvOperator(
            task_id=task_id,
            python_callable=MFA,
            op_args=[ORGANISM_NAME, GCF, chromosome_data],
            requirements=[
                "biopython",
                "matplotlib",
                "xlsxwriter",
                "openpyxl"
                # Add other dependencies as needed
            ],
        )

        # Set task dependencies if needed
        if i == 0:
            task.set_upstream(dag.get_task("load_org"))

        if i > 0:
            task.set_upstream(dag.get_task(f"MFA_{i}"))

        # TO DO: organism_id in chromosomes table
        # DAG for graphing