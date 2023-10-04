import json
import numpy as np


def write_json_dataset_to_neurons(neurons_merged):

    """Read from `analysis_dict['dict_match_dict']` and write a new dictionary
    to JSON file as follows:
        * each key is a dataset's name (e.g. '2022-06-14-01')
        * each value is another dictionary that maps neurons (e.g. 'RMDL')
        to their heatmap id in this dataset (following python's indexing
        convention)

    E.g. output:
    {
        "2022-06-14-01": {
            "RMDL": 4,
            "SMDDR": 56,
            ...
        }
        ...
    }
    """
    output_dict = dict()
    data_path = "/home/alicia/data3_personal/lab_metadata"
    with open(f"{data_path}/analysis_dict.json", "r") as f:
        dict_match_dict = json.load(f)['dict_match_dict']
    datasets = list(dict_match_dict.keys())
    for dataset in tqdm(datasets):
        output_dict[dataset] = dict()
        dataset_infos = dict_match_dict[dataset][0]
        for heatmap_id, info_dict in dataset_infos.items():
            if neurons_merged:
                output_dict[dataset][info_dict['neuron_class']] = \
                    int(heatmap_id) - 1
            else:
                output_dict[dataset][info_dict['label']] = int(heatmap_id) - 1

    if neurons_merged:
        file_name = "dataset_to_merged_neurons"
    else:
        file_name = "dataset_to_unmerged_neurons"

    with open(f'{data_path}/{file_name}.json', 'w') as f:
        json.dump(output_dict, f, indent=4)


def write_json_neuron_to_datasets(neurons_merged):

    # get unique neurons (either merged or unmerged)
    data_path = "/home/alicia/data3_personal/lab_metadata"
    if neurons_merged:
        input_file = "dataset_to_merged_neurons"
        output_file = "merged_neuron_to_datasets"
    else:
        input_file = "dataset_to_unmerged_neurons"
        output_file = "unmerged_neuron_to_datasets"

    with open(f"{data_path}/{input_file}.json", "r") as f:
        matches = json.load(f)
    all_neurons = []
    for info_dict in matches.values():
        all_neurons += list(info_dict.keys())
    unique_neurons = np.unique(all_neurons)

    # search for datasets that contains each neuron
    output_dict = dict()
    for neuron in unique_neurons:
        output_dict[neuron] = dict()

        for dataset, info_dict in matches.items():
            if neuron in info_dict.keys():
                output_dict[neuron][dataset] = info_dict[neuron]

    with open(f'{data_path}/{output_file}.json', 'w') as f:
        json.dump(output_dict, f, indent=4)
