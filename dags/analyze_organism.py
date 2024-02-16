from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonVirtualenvOperator, PythonOperator
from airflow.operators.empty import EmptyOperator


def _set_path():
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def load_organism(organism_name, gcf, amount_chromosomes):
    _set_path()
    from src.Biocode.managers.DBConnectionManager import DBConnectionManager
    from src.Biocode.services.OrganismsService import OrganismsService

    print("Entered task")
    DBConnectionManager.start()
    organism_service = OrganismsService()
    organism_service.insert(record=(organism_name, gcf, amount_chromosomes))
    DBConnectionManager.close()


def whole_MFA(organism_name, gcf, chromosome):
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
    genome_manager = GenomeManager(genome_data=[chromosome], organism_name=organism_name)
    genome_manager.calculate_multifractal_analysis_values()
    genome_manager.save_to_db(GCF=gcf)
    genome_manager.generate_df_results()

    print(genome_manager.get_mfa_results())
    DBConnectionManager.close()


def regions_MFA(organism_name, gcf, chromosome, regions_number):
    try:
        import os
        import sys
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from src.Biocode.managers.RegionGenomeManager import RegionGenomeManager
        from src.Biocode.managers.DBConnectionManager import DBConnectionManager
    except ImportError as e:
        print(f"Error importing necessary modules: {e}")
        raise

    DBConnectionManager.start()
    region_genome_manager = RegionGenomeManager(genome_data=[chromosome], organism_name=organism_name,
                                                regions_number=regions_number)
    region_genome_manager.calculate_multifractal_analysis_values()
    region_genome_manager.save_to_db(GCF=gcf)
    region_genome_manager.generate_df_results()

    print(region_genome_manager.get_mfa_results())
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
    from src.load import data, ORGANISM_NAME, GCF, AMOUNT_CHROMOSOMES, REGIONS_NUMBER

    t1 = PythonOperator(task_id="load_org",
                        python_callable=load_organism,
                        op_args=[ORGANISM_NAME, GCF, AMOUNT_CHROMOSOMES])

    whole_tasks_amount = 0
    for i, chromosome_data in enumerate(data):
        task_id = f"whole_{i + 1}"
        task = PythonVirtualenvOperator(
            task_id=task_id,
            python_callable=whole_MFA,
            op_args=[ORGANISM_NAME, GCF, chromosome_data],
            requirements=[
                "biopython",
                "xlsxwriter",
                "openpyxl",
                "matplotlib"
                # Add other dependencies as needed
            ],
        )

        # Set task dependencies if needed
        if i == 0:
            task.set_upstream(dag.get_task("load_org"))

        if i > 0:
            task.set_upstream(dag.get_task(f"whole_{i}"))
            whole_tasks_amount += 1

    empty = EmptyOperator(task_id="whole_end")
    empty.set_upstream(dag.get_task(f"whole_{len(data)}"))

    for i, chromosome_data in enumerate(data):
        task_id = f"regions_{i + 1}"
        task = PythonVirtualenvOperator(
            task_id=task_id,
            python_callable=regions_MFA,
            op_args=[ORGANISM_NAME, GCF, chromosome_data, REGIONS_NUMBER],
            requirements=[
                "biopython",
                "xlsxwriter",
                "openpyxl",
                "matplotlib"
                # Add other dependencies as needed
            ],
        )

        # Set task dependencies if needed
        if i == 0:
            task.set_upstream(dag.get_task(f"load_org"))

        if i > 0:
            task.set_upstream(dag.get_task(f"regions_{i}"))

    empty = EmptyOperator(task_id="regions_end")
    empty.set_upstream(dag.get_task(f"regions_{len(data)}"))
    # DAG for graphing
