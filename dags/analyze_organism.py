from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonVirtualenvOperator


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
    c_elegans_manager.calculate_multifractal_analysis_values()
    print(c_elegans_manager.get_mfa_results())
    print("SUCCESS")


with DAG("analyze_organism", description="MFA of organism",
         start_date=datetime(2024, 1, 15), schedule_interval="@once") as dag:
    """
    1. Read xlsx file and read organism info and GCF.
    2. Download the organism genome.
    3. Execute the code.
    4. Keep the files and data.
    """
    from src.load import c_elegans_data

    for i, chromosome_data in enumerate(c_elegans_data):
        task_id = f"MFA_{i}"
        t1 = PythonVirtualenvOperator(
            task_id=task_id,
            python_callable=MFA,
            op_args=["Caenorhabditis elegans", chromosome_data],
            requirements=[
                "biopython",
                "matplotlib"
                # Add other dependencies as needed
            ],
        )

        # Set task dependencies if needed

        if i > 0:
            t1.set_upstream(dag.get_task(f"MFA_{i - 1}"))