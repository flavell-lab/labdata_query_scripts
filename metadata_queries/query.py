from metadata_queries.search import *
from pprint import pprint
import argparse


def main():

    parser = argparse.ArgumentParser(description="a query toolkit")

    # Use '-d' or '--datasets' flag for datasets
    parser.add_argument('-d', '--datasets', type=str, nargs='+',
                        help='List of dataset strings like "2022-06-14-01"')

    # Use '-n' or '--neurons' flag for neuron names
    parser.add_argument('-n', '--neurons', type=str, nargs='+',
                        help='List of neuron names like "AVB"')

    args = parser.parse_args()
    if args.datasets:
        pprint(find_common_neurons_for_datasets(args.datasets))
    if args.neurons:
        pprint(find_common_datasets_for_neurons(args.neurons))


if __name__ == "__main__":
    main()
