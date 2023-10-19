from itertools import chain, combinations
import json
import re


def find_common_neurons_for_datasets(datasets):

    """Find all the neurons (merged and unmerged) that are contained in the
    given datasets and output a dictionary structured as follows:
        {
            neuron_A: {
                        dataset_1: index1,
                        dataset_2: index2,
                        …
            }
            …
        }
    """
    data_path = "lab_metadata"

    with open(f"{data_path}/dataset_to_unmerged_neurons.json", "r") as f:
        matches_unmerged = json.load(f)
    with open(f"{data_path}/dataset_to_merged_neurons.json", "r") as f:
        matches_merged = json.load(f)

    # find common neurons shared by the datasets

    all_merged_neurons = []
    all_unmerged_neurons = []
    for dataset in datasets:
        all_merged_neurons.append(list(matches_merged[dataset].keys()))
        all_unmerged_neurons.append(list(matches_unmerged[dataset].keys()))

    set_of_merged_neurons = [set(neurons) for neurons in all_merged_neurons]
    common_merged_neurons = list(set.intersection(*set_of_merged_neurons))

    set_of_unmerged_neurons = [set(neurons) for neurons in all_unmerged_neurons]
    common_unmerged_neurons = list(set.intersection(*set_of_unmerged_neurons))

    # format the output dictionary

    output_dict = dict()
    for merged_neuron in common_merged_neurons:
        output_dict[merged_neuron] = dict()

        for dataset in datasets:
            output_dict[merged_neuron][dataset] = \
                matches_merged[dataset][merged_neuron]

    for unmerged_neuron in common_unmerged_neurons:
        output_dict[unmerged_neuron] = dict()

        for dataset in datasets:
            output_dict[unmerged_neuron][dataset] = \
                matches_unmerged[dataset][unmerged_neuron]

    return output_dict


def find_common_datasets_for_neurons(neurons):

    """Find the common datasets that contain all of the given neurons and
    output a dictionary structured as follows:
        {
            dataset_name: {
                neuron_A: indexA,
                neuron_B: indexB,
                …
            }
            …
        }
    """
    data_path = "lab_metadata"

    with open(f"{data_path}/unmerged_neuron_to_datasets.json", "r") as f:
        matches_unmerged = json.load(f)
        unmerged_neurons = list(matches_unmerged.keys())
    with open(f"{data_path}/merged_neuron_to_datasets.json", "r") as f:
        matches_merged = json.load(f)
        merged_neurons = list(matches_merged.keys())

    # find common datasets shared by the neurons

    all_datasets = []
    for neuron in neurons:
        if neuron in unmerged_neurons:
            all_datasets.append(list(matches_unmerged[neuron].keys()))
        elif neuron in merged_neurons:
            all_datasets.append(list(matches_merged[neuron].keys()))
        else:
            print(f"{neuron} is not found")

    sets_of_datasets = [set(datasets) for datasets in all_datasets]
    common_datasets = list(set.intersection(*sets_of_datasets))

    # format the output dictionary

    output_dict = dict()
    for common_dataset in common_datasets:
        output_dict[common_dataset] = dict()

        for neuron in neurons:
            if neuron in unmerged_neurons:
                neuron_index = matches_unmerged[neuron][common_dataset]
            elif neuron in merged_neurons:
                neuron_index = matches_merged[neuron][common_dataset]
            else:
                continue

            output_dict[common_dataset][neuron] = neuron_index

    return output_dict


def find_common_datasets_for_flex_neurons(neurons):

    """Find all the datasets that contains either the given neurons or the
    'flexible' versions of the given neurons; for instance, if one of the given
    neurons is `SMD`, the function seeks datasets that contain `SMDD?`,
    `SMDDL`, `SMDDR`, `SMDVL`, and `SMDVR`.
    The output dictionary is structured as follows:
        {
            dataset_name: {
                neuron_A: indexA,
                neuron_B: indexB,
                …
            }
            …
        }
    """
    data_path = "/home/alicia/data3_personal/lab_metadata"
    with open(f"{data_path}/unmerged_neuron_to_datasets.json", "r") as f:
        matches_unmerged = json.load(f)

    patterns = [re.compile(neuron + ".*") for neuron in neurons]
    subset_matches_unmerged = dict()

    # create subset information dictionary whose keys are the flexible neuron
    # names (meaning they don't have to match exactly with the given neurons),
    # whose values are the datasets containing the flexible neuron

    for pattern in patterns:
        for neuron, datasets in matches_unmerged.items():
            if pattern.search(neuron):
                subset_matches_unmerged[neuron] = datasets

    # find common datasets shared by the neurons

    flex_neurons = list(subset_matches_unmerged.keys())

    subset_dataset_list = find_common_datasets_for_neuron_subsets(
                flex_neurons,
                subset_matches_unmerged
    )

    # format the output dictionary

    output_dict = dict()

    for neuron_subset, common_datasets in subset_dataset_list:

        subset_name = "-".join(neuron_subset)
        output_dict[subset_name] = dict()

        for common_dataset in common_datasets:
            output_dict[subset_name][common_dataset] = dict()

            for neuron in neuron_subset:
                neuron_index = subset_matches_unmerged[neuron][common_dataset]
                output_dict[subset_name][common_dataset][neuron] = neuron_index

    return output_dict


def find_common_datasets_for_neuron_subsets(neurons, matches):

    """Find the nonempty datasets for subsets of the given neurons

    Args:
        neurons: a list of neuron names
        matches: a dictionary with neuron names as keys, the datasets
            containing them as values; it is structured as follows:
                {
                    neuron_A: {
                                dataset_1: index1,
                                dataset_2: index2,
                                …
                    }
                    …
                }
    """
    all_subsets = powerset(neurons)
    max_num_common_datasets = 0
    max_common_datasets = []
    best_subset = []
    output_list = []

    for subset in all_subsets:

        all_datasets = []
        for neuron in subset:
            all_datasets.append(list(matches[neuron].keys()))

        sets_of_datasets = [set(datasets) for datasets in all_datasets]
        common_datasets = list(set.intersection(*sets_of_datasets))

        if len(common_datasets) > 0:
            output_list.append((subset, common_datasets))

        if len(common_datasets) >= max_num_common_datasets:
            max_num_common_datasets = len(common_datasets)
            max_common_datasets[:] = common_datasets
            best_subset[:] = subset

    return output_list


def powerset(iterable):

    s = list(iterable)
    all_combinations = list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))

    return [subset for subset in all_combinations if len(subset) > 0]

