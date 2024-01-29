from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
import subprocess


def _set_path():
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def load_data_whole():
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
    # subprocess.check_call(["pip", "install", "matplotlib"])

    # Push the DataFrame to XCom
    return df.to_dict(orient='records')


def load_data_regions():
    try:
        _set_path()
        from src.Biocode.services.RegionResultsService import RegionResultsService
        from src.Biocode.managers.DBConnectionManager import DBConnectionManager
    except ImportError as e:
        print(f"Error importing necessary modules: {e}")
        raise

    DBConnectionManager.start()
    region_results_service = RegionResultsService()
    df = region_results_service.extract_results()
    DBConnectionManager.close()
    print(df)
    # Install required packages
    # subprocess.check_call(["pip", "install", "matplotlib"])

    # Push the DataFrame to XCom
    return df.to_dict(orient='records')


def graph_whole(**context):
    # Install required packages
    subprocess.check_call(["pip", "install", "biopython"])
    _set_path()
    from src.Biocode.managers.GenomeManager import GenomeManager
    from src.load import c_elegans_data
    from src.Biocode.utils.utils import str_to_list
    from analyze_organism import ORGANISM_NAME

    genome_manager = GenomeManager(genome_data=c_elegans_data, organism_name=ORGANISM_NAME)

    ti = context["ti"]
    output = ti.xcom_pull(task_ids="load_data_whole")
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


def graph_regions(**context):
    # Install required packages
    subprocess.check_call(["pip", "install", "biopython"])
    _set_path()
    from src.Biocode.managers.RegionGenomeManager import RegionGenomeManager
    from src.load import c_elegans_data
    from src.Biocode.utils.utils import str_to_list
    from analyze_organism import ORGANISM_NAME, REGIONS_NUMBER

    region_genome_manager = RegionGenomeManager(genome_data=c_elegans_data, organism_name=ORGANISM_NAME,
                                                regions_number=REGIONS_NUMBER)

    ti = context["ti"]
    output = ti.xcom_pull(task_ids="load_data_regions")
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

    cover = [str_to_list(item['cover']) for item in output]
    cover_percentage = [item['cover_percentage'] for item in output]
    degrees_of_multifractality = [item['DDq'] for item in output]

    region_genome_manager.set_mfa_results(mfa_results)
    region_genome_manager.set_flattened_mfa_results(mfa_results)
    region_genome_manager.set_cover(cover)
    region_genome_manager.set_cover_percentage(cover_percentage)
    region_genome_manager.set_degrees_of_multifractality(degrees_of_multifractality)

    region_genome_manager.graph_degrees_of_multifractality()
    region_genome_manager.graph_multifractal_analysis_merged()


with DAG("graph_organism", description="Graphs of organism",
         start_date=datetime(2024, 1, 15), schedule_interval="@once") as dag:
    sensor_whole = ExternalTaskSensor(task_id="waiting_dag_whole",
                                      external_dag_id="analyze_organism",
                                      external_task_id="whole_end",
                                      poke_interval=200
                                      )

    load_whole = PythonOperator(task_id="load_data_whole",
                                python_callable=load_data_whole,
                                provide_context=True,  # Enable passing context to the callable
                                )

    whole_graphs = PythonOperator(
        task_id="whole_graphs",
        python_callable=graph_whole,
        provide_context=True,
    )

    sensor_regions = ExternalTaskSensor(task_id="waiting_dag_regions",
                                        external_dag_id="analyze_organism",
                                        external_task_id="regions_end",
                                        poke_interval=200)

    load_regions = PythonOperator(task_id="load_data_regions",
                                  python_callable=load_data_regions,
                                  provide_context=True)

    regions_graphs = PythonOperator(task_id="regions_graphs",
                                    python_callable=graph_regions,
                                    provide_context=True)

    sensor_whole >> load_whole >> whole_graphs
    sensor_regions >> load_regions >> regions_graphs
