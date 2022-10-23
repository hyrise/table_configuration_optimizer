# Table Configuration Optimizer 

This repository contains source code and artifacts for the paper "Budget-Conscious Fine-Grained Configuration Optimization for Spatio-Temporal Applications" (VLDB 2022). It includes the different presented linear programming models to jointly optimize the sorting, compression, indexing, and tiering decisions for spatio-temporal applications. 

In case you have any questions, please contact [Keven Richly](https://hpi.de/plattner/people/phd-students/keven-richly.html).

### Citation

Shortened DBLP BibTeX entry:
```bibtex
@article{DBLP:journals/pvldb/Richly22,
  author    = {Keven Richly and Rainer Schlosser and Martin Boissier},
  title     = {Budget-Conscious Fine-Grained Configuration Optimization for Spatio-Temporal Applications},
  journal   = {Proc. {VLDB} Endow.},
  volume    = {15},
  number    = {13},
  pages     = {4079 - 4092},
  year      = {2022},
  url       = {tba},
  doi       = {10.14778/3565838.3565858}
}
```

## Setup

To get all dependencies of the Table Configuration Optimizer installed, run

    pip install -r requirements.txt

To start the jupyter lab, run

    jupyter lab

Additionally, it is required to have a solver, such as [gurobi](https://www.gurobi.com), installed. Also, other common free linear programming solvers ([GLPK](https://www.gnu.org/software/glpk/) or [LP_Solve](https://sourceforge.net/projects/lpsolve/)) can be used. In this context, the solve times of the different solvers can vary strongly.

## Linear Programming Models

To efficiently utilize the scarce DRAM capacities, modern database systems support various tuning possibilities to reduce the memory footprint or increase performance. However, the selection of cost and performance-balancing configurations is challenging due to the vast number of possible setups consisting of mutually dependent individual decisions. We introduce a novel approach to jointly optimize the compression, sorting, indexing, and tiering configuration for spatio-temporal workloads. Further, we consider horizontal data partitioning, which enables the independent application of different tuning options on a fine-grained level. We propose three different linear programming (LP) models addressing cost dependencies at different levels of accuracy to compute optimized tuning configurations for a given workload and memory budgets:

  - The [Segment-Based Model with Sorting Dependencies (SMS)](https://github.com/hyrise/table_configuration_optimizer/blob/main/models/sms_model.ipynb) allows to solve the configuration problem with segment-based costs. It includes intra-chunk dependencies between segments with regard to the chunk-based ordering decision.
  - The [Relaxed Model with Independent Segment Effects (ISE)](https://github.com/hyrise/table_configuration_optimizer/blob/main/models/ise_model.ipynb) uses a relaxation regarding the ordering dependencies of the cost effects between segments to solve the SMS model heuristically.
  - The [General Model with Chunk-based Configuration Dependencies (CCD)](https://github.com/hyrise/table_configuration_optimizer/blob/main/models/ccd_model.ipynb) is a solution approach accounting for full cost dependencies within a chunk. In this model, the costs associated with a segment can depend on all specific configuration decisions of all other segments (enabling the inclusion of multi-attribute indexes, etc.).

To yield maintainable and robust configurations, we extend our LP-based approach to incorporate reconfiguration costs as well as a worst-case optimization for potential workload scenarios. The extended LP models for the SMS and ISE models can be found here:

  - Minimal-invasive state-dependent reconfigurations ([SMS](https://github.com/hyrise/table_configuration_optimizer/blob/main/models/sms_model_reconfiguration_costs.ipynb), [ISE](https://github.com/hyrise/table_configuration_optimizer/blob/main/models/ise_model_reconfiguration_costs.ipynb))
  - Robust configuration selection for different potential workload scenarios ([SMS](https://github.com/hyrise/table_configuration_optimizer/blob/main/models/sms_model_robust.ipynb), [ISE](https://github.com/hyrise/table_configuration_optimizer/blob/main/models/ise_model_robust.ipynb))

## Example: Transportation Network Company

To demonstrate the impact of different tuning decisions on the memory consumption and the runtime of a scan operation, as well as for the evaluation of our optimization approaches, we use the real-world dataset of a transportation network company (TNC) as an example. The spatio-temporal dataset consists of 400 million observed locations of drivers for three consecutive months in the City of Dubai (raw size 15.9 GB). Besides the timestamp, latitude, longitude, and the driver's identifier, a status attribute is tracked for each observed location. The status indicates the driver's current state (free or occupied). All attributes are stored as integers. Based on the insertion order, a certain temporal ordering of the sample points exists, but we cannot guarantee that the timestamp column is sorted due to transmission problems and delayed transmissions. 

### Data

The [data](https://github.com/hyrise/table_configuration_optimizer/tree/main/data) folder provides the necessary input data for the models determined for the dataset of a TNC. All end-to-end measurements have been executed on a server equipped with Intel Xeon Platinum 8180 CPUs (2.50GHz). For the benchmark queries and the evaluation of the determined configurations, we use the research database [Hyrise](https://github.com/hyrise/hyrise). We define the input parameters based on the supported encoding and indexing properties of the database. It contains the measured runtimes of the benchmark queries, DRAM consumption of the different encodings, and the results of the calibrations queries (storage penalty, consecutive scan penalty). We explain how to determine these parameters for other datasets and workloads with Hyrise [here](). 

### Workload 

For the evaluation presented in the paper, we used a workload consisting of six query templates to evaluate the models based on the data of a TNC.

| ID            | Query            | Frequency | Skipped Chunks   |
| ------------- | ---------------- | --------- | ---------------- |
| q<sub>0</sub> | SELECT * FROM TABLE WHERE <br> ("driver_id" <= {selectivity of the value: 0.0001}) AND <br> ("status" <= {0.7}) | 15%       | 0, 1 |
| q<sub>1</sub> | SELECT * FROM TABLE WHERE <br> ("timestamp" BETWEEN {0.2}) AND <br> ("latitude" BETWEEN {0.5}) AND <br> ("longitude" BETWEEN {0.5}) AND <br> ("status" <= {0.7}) | 15%       | 0, 1, 2, 6, 7, 8, 9 |
| q<sub>2</sub> | SELECT * FROM TABLE WHERE <br> („driver_id" <= {0.01}) AND <br> ("latitude" BETWEEN {0.1}) AND <br> ("longitude" BETWEEN {0.1}) | 10%       |  |
| q<sub>3</sub> | SELECT * FROM TABLE WHERE <br> ("timestamp" <= {0.05}) AND <br> ("latitude" BETWEEN {0.7}) AND <br> ("longitude" BETWEEN {0.7}) | 25%       | 1, 2, 3, 4, 5, 6, 7, 8, 9 |
| q<sub>4</sub> | SELECT * FROM TABLE WHERE <br> („driver_id" <= {0.01}) AND <br> ("timestamp" <= {0.4}) | 15%       | 4, 5, 6, 7, 8, 9 |
| q<sub>5</sub> | SELECT * FROM TABLE WHERE <br> ("latitude" BETWEEN {0.01}) AND <br> ("longitude" BETWEEN {0.01}) AND <br> ("timestamp" BETWEEN {0.5}) | 20%       | 0, 1, 8, 9 |

Further workload examples are provided in `/data/workloads`. 

## Evaluation in Hyrise

To evaluate the performance of the determined table configurations for a given dataset and workload in Hyrise, we provide a benchmark in the  `krichly/chunk_sort_compression_advanced` branch. The benchmark is implemented in the playground of Hyrise that is stored at `src/bin/playground.cpp`. To execute the benchmark, it is necessary to setup Hyrise. A step-by-step guide to get, setup, and run Hyrise is provided [here](https://github.com/hyrise/hyrise/wiki/Step-by-Step-Guide). The playground is built with the following command:

  make hyrisePlayground

As input for the benchmark, the user has to provide a set of table configurations determined by the models and exported as .csv files, the workload, and the dataset in the `data` folder. The benchmark is executed with the command: 

  ./hyrisePlayground

For each table configuration, the benchmark applies the defined tuning options (compression, indexing, sorting, and tiering configuration) and executes the workload on the table. Afterward, the performance (runtime of each query) and the memory consumption of each table configuration are exported as .csv file.

Furthermore, we implemented a microbenchmark in `src/benchmark/ping_data_micro_benchmark.cpp` that determines for a given dataset the input parameters for the models (runtime and memory consumption). To build the microbenchmarks, the following command is used:  

  make hyriseMicroBenchmarks

Based on the dataset, the chunk size and the column names have to be adjusted. The benchmark can be executed by the command:  

  ./hyriseMicroBenchmarks --benchmark_out=../../out/performance.csv --benchmark_out_format=csv --benchmark_repetitions=5 --benchmark_filter="BM_PingData" --benchmark_min_time=5 --benchmark_display_aggregates_only=true
