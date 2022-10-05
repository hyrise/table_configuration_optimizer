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
  pages     = {tba},
  year      = {2022},
  url       = {tba},
  doi       = {tba}
}
```

## Setup

To get all dependencies of the Table Configuration Optimizer installed, run

    pip install -r requirements.txt

To start the jupyter lab, run

    jupyter lab

Additionally, it is required to have a solver, such as [gurobi](https://www.gurobi.com), installed.

## Example: Data

The data folder provides the necessary input data for the models determined for the dataset of a transportation network company. All end-to-end measurements have been executed on a server equipped with Intel Xeon Platinum 8180 CPUs (2.50GHz). For the benchmark queries and the evaluation of the determined configurations, we use the research database [Hyrise](https://github.com/hyrise/hyrise). We define the input parameters based on the supported encoding and indexing properties of the database. It contains the measured runtimes of the benchmark queries, DRAM consumption of the different encodings, and the results of the calibrations queries.

## Example: Workload 

We used a workload consisting of six query templates to evaluate the models based on the data of a transportation network company. 

| ID            | Query            | Frequency | Skipped Chunks   |
| ------------- | ---------------- | --------- | ---------------- |
| q<sub>0</sub> | SELECT * FROM TABLE WHERE <br> ("driver_id" <= {selectivity of the value: 0.0001}) AND <br> ("status" <= {0.7}) | 15%       | 0, 1 |
| q<sub>1</sub> | SELECT * FROM TABLE WHERE <br> ("timestamp" BETWEEN {0.2}) AND <br> ("latitude" BETWEEN {0.5}) AND <br> ("longitude" BETWEEN {0.5}) AND <br> ("status" <= {0.7}) | 15%       | 0, 1, 2, 6, 7, 8, 9 |
| q<sub>2</sub> | SELECT * FROM TABLE WHERE <br> („driver_id" <= {0.01}) AND <br> ("latitude" BETWEEN {0.1}) AND <br> ("longitude" BETWEEN {0.1}) | 10%       |  |
| q<sub>3</sub> | SELECT * FROM TABLE WHERE <br> ("timestamp" <= {0.05}) AND <br> ("latitude" BETWEEN {0.7}) AND <br> ("longitude" BETWEEN {0.7}) | 25%       | 1, 2, 3, 4, 5, 6, 7, 8, 9 |
| q<sub>4</sub> | SELECT * FROM TABLE WHERE <br> („driver_id" <= {0.01}) AND <br> ("timestamp" <= {0.4}) | 15%       | 4, 5, 6, 7, 8, 9 |
| q<sub>5</sub> | SELECT * FROM TABLE WHERE <br> ("latitude" BETWEEN {0.01}) AND <br> ("longitude" BETWEEN {0.01}) AND <br> ("timestamp" BETWEEN {0.5}) | 20%       | 0, 1, 8, 9 |

Further workload examples are provided in `/data/workloads`. 


