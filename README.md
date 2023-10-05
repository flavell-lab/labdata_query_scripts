# FlavellLab: Whole-Brain Imaging Metadata Query Toolkit
A toolkit designed for effortlessly querying metadata from whole-brain imaging datasets using intuitive command-line instructions

## table of contents
- [installation](#installation)
- [usage](#usage)
    - [Provide specific datasets and query for neurons common to them](#provide-specific-datasets-and-query-for-neurons-common-to-them)
        - [command to run](#command-to-run)
        - [output](#output)
        - [example](#example)
    - [Provide specific neurons and query for datasets associated with them](#provide-specific-neurons-and-query-for-datasets-associated-with-them)
        - [command to run](#command-to-run-1)
        - [output](#output-1)
        - [example](#example-1)
- [caveat](#caveat)

## installation
To install the package locally, run the following commands
```console
$ git clone https://github.com/flavell-lab/labdata_query_scripts.git
$ cd labdata_query_scripts
$ pip install .
```
To install on `flv-c2` or `flv-c3`, run the following commands
```console
$ git clone git@github.com:flavell-lab/labdata_query_scripts.git
$ cd labdata_query_scripts
$ pip install .
```

## usage
Make sure to be in the `metadata_queries` directory; you can do so by running
```console
$ cd metadata_queries
```
To acquire dataset information, you can:
##### Provide specific datasets and query for neurons common to them
###### command to run
  ```console
  $ python query.py -d dataset1 dataset2 dataset3
  ```
###### output
  ```py
  {
    neuronA: {
        dataset1: neuronA_heatmapID_in_dataset1
        dataset2: neuronA_heatmapID_in_dataset2
        dataset3: neuronA_heatmapID_in_dataset3
    }
    neuronB: {
        dataset1: neuronB_heatmapID_in_dataset1
        dataset2: neuronB_heatmapID_in_dataset2
        dataset3: neuronB_heatmapID_in_dataset3
    }
    ...
  }
  ```
###### example
```console
$ python query.py -d 2023-01-23-15 2023-01-19-22 2023-01-19-08
```
returns
```py
{'ADE': {'2022-07-26-01': 32,
         '2023-01-09-15': 17,
         '2023-01-18-01': 52,
         '2023-01-19-08': 139,
         '2023-01-19-22': 139,
         '2023-01-23-15': 145},
 'ADEL': {'2022-07-26-01': 32,
          '2023-01-09-15': 17,
          '2023-01-18-01': 52,
          '2023-01-19-08': 139,
          '2023-01-19-22': 139,
          '2023-01-23-15': 54},
 'AIB': {'2022-07-26-01': 96,
         '2023-01-09-15': 79,
         '2023-01-18-01': 73,
         '2023-01-19-08': 113,
         '2023-01-19-22': 128,
         '2023-01-23-15': 132},
    ...
}
```


##### Provide specific neurons and query for datasets associated with them

###### command to run
  ```console
  $ python query.py -d neuronA neuronB neuronC
  ```
###### output
```py
  {
    dataset1: {
        neuronA: neuronA_heatmapID_in_dataset1
        neuronB: neuronA_heatmapID_in_dataset1
        neuronC: neuronA_heatmapID_in_dataset1
    }
    dataset2: {
        neuronA: neuronB_heatmapID_in_dataset2
        neuronB: neuronB_heatmapID_in_dataset2
        neuronC: neuronB_heatmapID_in_dataset2
    }
    ...
  }
```
###### example
  ```console
  $ python query.py -n URBL SMB RMDVL OLQVR RIA
  ```
 returns
  ```py
  {'2022-06-14-01': {'OLQVR': 83,
                   'RIA': 107,
                   'RMDVL': 10,
                   'SMB': 88,
                   'URBL': 101},
 '2022-07-15-12': {'OLQVR': 34,
                   'RIA': 116,
                   'RMDVL': 30,
                   'SMB': 63,
                   'URBL': 122},
 '2022-07-20-01': {'OLQVR': 114, 'RIA': 37, 'RMDVL': 82, 'SMB': 98, 'URBL': 40},
 '2022-07-26-01': {'OLQVR': 63, 'RIA': 79, 'RMDVL': 91, 'SMB': 6, 'URBL': 105},
 '2023-01-05-18': {'OLQVR': 116, 'RIA': 24, 'RMDVL': 88, 'SMB': 90, 'URBL': 16},
 '2023-01-09-15': {'OLQVR': 27, 'RIA': 123, 'RMDVL': 9, 'SMB': 145, 'URBL': 88},
 '2023-01-18-01': {'OLQVR': 95, 'RIA': 40, 'RMDVL': 97, 'SMB': 71, 'URBL': 37},
 '2023-01-19-08': {'OLQVR': 42,
                   'RIA': 119,
                   'RMDVL': 86,
                   'SMB': 15,
                   'URBL': 127},
 '2023-01-19-22': {'OLQVR': 79, 'RIA': 87, 'RMDVL': 53, 'SMB': 127, 'URBL': 82},
 '2023-01-23-15': {'OLQVR': 104,
                   'RIA': 102,
                   'RMDVL': 136,
                   'SMB': 130,
                   'URBL': 105}}
  ```

  ## caveat
The heatmap ID for neurons follows Python's indexing convention, where the first index starts at 0. Note: If you're coding in Julia, indices start at 1! Ensure you adjust by adding 1 to the index accordingly.
