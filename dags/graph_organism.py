from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
import subprocess

from analyze_organism import amount_tasks

AMOUNT_ANALYZE_TASKS = amount_tasks - 2


def _set_path():
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def load_data():
    try:
        _set_path()
        from src.Biocode.services.WholeResultsService import WholeResultsService
        from src.Biocode.managers.DBConnectionManager import DBConnectionManager
    except ImportError as e:
        print(f"Error importing necessary modules: {e}")
        raise

    DBConnectionManager.start()
    whole_results_service = WholeResultsService()
    df = whole_results_service.extract_results()
    DBConnectionManager.close()

    # Install required packages
    subprocess.check_call(["pip", "install", "matplotlib"])

    # Push the DataFrame to XCom
    return df.to_dict(orient='records')


def graph(**context):
    # Install required packages
    subprocess.check_call(["pip", "install", "biopython"])
    _set_path()
    from src.Biocode.managers.GenomeManager import GenomeManager
    from src.load import c_elegans_data
    from src.Biocode.utils.utils import str_to_list

    genome_manager = GenomeManager(genome_data=c_elegans_data, organism_name="Caenorhabditis elegans")

    ti = context["ti"]
    output = ti.xcom_pull(task_ids="load_data")
    desired_keys_ddq = ['DDq', 'sequence_name']
    desired_keys_dq_tauq = ['Dq_values', 'tau_q_values']

    mfa_results = []

    for item in output:
        result_entry = {
            'q_values': list(range(-20, 21)),
            **{key: item[key] for key in desired_keys_ddq}
        }

        result_entry.update({
            key: str_to_list(item[key]) for key in desired_keys_dq_tauq
        })

        mfa_results.append(result_entry)

    cover = [item['cover'] for item in output]
    cover_percentage = [item['cover_percentage'] for item in output]
    degrees_of_multifractality = [item['DDq'] for item in output]

    genome_manager.set_mfa_results(mfa_results)
    genome_manager.set_cover(cover)
    genome_manager.set_cover_percentage(cover_percentage)
    genome_manager.set_degrees_of_multifractality(degrees_of_multifractality)

    genome_manager.graph_degrees_of_multifractality()
    genome_manager.graph_multifractal_analysis_merged()


with DAG("graph_organism", description="Graphs of organism",
         start_date=datetime(2024, 1, 15), schedule_interval="@once") as dag:
    sensor = ExternalTaskSensor(task_id="waiting_dag",
                                external_dag_id="analyze_organism",
                                external_task_id="MFA_end",
                                poke_interval=10
                                )

    load = PythonOperator(task_id="load_data",
                          python_callable=load_data,
                          provide_context=True,  # Enable passing context to the callable
                          )

    task = PythonOperator(
        task_id="Graphs",
        python_callable=graph,
        provide_context=True,
    )

    sensor >> load >> task
