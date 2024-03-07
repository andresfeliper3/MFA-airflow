def _set_path():
    import os
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def load_data_whole():
    try:
        _set_path()
        from src.Biocode.services.WholeResultsService import WholeResultsService
        from src.Biocode.managers.DBConnectionManager import DBConnectionManager
        from src.load import GCF
    except ImportError as e:
        print(f"Error importing necessary modules: {e}")
        raise

    DBConnectionManager.start()
    whole_results_service = WholeResultsService()
    df = whole_results_service.extract_results(GCF=GCF)
    DBConnectionManager.close()

    # Push the DataFrame to XCom
    return df.to_dict(orient='records')


def graph_whole(**context):
    _set_path()
    from src.Biocode.managers.GenomeManager import GenomeManager
    from src.load import data, ORGANISM_NAME
    from src.Biocode.utils.utils import str_to_list

    genome_manager = GenomeManager(genome_data=data, organism_name=ORGANISM_NAME)

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

    cover = [str_to_list(item['cover']) for item in output]
    cover_percentage = [item['cover_percentage'] for item in output]
    degrees_of_multifractality = [item['DDq'] for item in output]

    genome_manager.set_mfa_results(mfa_results)
    genome_manager.set_cover(cover)
    genome_manager.set_cover_percentage(cover_percentage)
    genome_manager.set_degrees_of_multifractality(degrees_of_multifractality)

    genome_manager.generate_df_results()

    genome_manager.graph_degrees_of_multifractality()
    genome_manager.graph_multifractal_analysis_merged()

    genome_manager.graph_coverage()
