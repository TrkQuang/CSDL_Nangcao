# Benchmark Summary

Index No = constraint-backed indexes retained. Index Yes = benchmark secondary indexes added.
Warm cache; one warm-up and recorded repeats. Writes rolled back to savepoints.
INSERT adds a child of node 2; UPDATE moves leaf N below node 2, not a whole subtree.

## Q2_Subtree

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 1.202 | 0.119 | 63.000 | 0.000 |
| Adjacency List | Yes | 1.513 | 0.198 | 63.000 | 0.000 |
| Path Enumeration | No | 0.592 | 0.102 | 15.000 | 0.000 |
| Path Enumeration | Yes | 0.174 | 0.123 | 19.000 | 0.000 |
| Nested Set | No | 0.645 | 0.099 | 9.000 | 0.000 |
| Nested Set | Yes | 0.197 | 0.159 | 12.000 | 0.000 |
| Closure Table | No | 0.149 | 0.063 | 10.000 | 0.000 |
| Closure Table | Yes | 0.275 | 0.173 | 12.000 | 0.000 |

## INSERT_Leaf

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.323 | 0.010 | 26.000 | 0.000 |
| Adjacency List | Yes | 0.153 | 0.006 | 28.000 | 0.000 |
| Path Enumeration | No | 0.641 | 0.011 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.356 | 0.006 | 46.000 | 0.000 |
| Nested Set | No | 20.266 | 0.037 | 18255.000 | 0.000 |
| Nested Set | Yes | 22.087 | 0.012 | 22321.000 | 0.000 |
| Closure Table | No | 0.915 | 0.012 | 100.000 | 0.000 |
| Closure Table | Yes | 0.506 | 0.007 | 83.000 | 0.000 |

## UPDATE_MoveLeaf

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.390 | 0.007 | 32.000 | 0.000 |
| Adjacency List | Yes | 0.259 | 0.006 | 38.000 | 0.000 |
| Path Enumeration | No | 0.463 | 0.007 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.360 | 0.006 | 55.000 | 0.000 |
| Nested Set | No | 21.932 | 0.013 | 21745.000 | 0.000 |
| Nested Set | Yes | 28.591 | 0.012 | 24943.000 | 0.000 |
| Closure Table | No | 1.258 | 0.006 | 137.000 | 0.000 |
| Closure Table | Yes | 0.565 | 0.007 | 96.000 | 0.000 |

## Storage

Table bytes exclude indexes and TOAST; total bytes include auxiliary storage.

| Nodes | Secondary index | Relation | Table bytes | Index bytes | Total bytes |
| ---: | --- | --- | ---: | ---: | ---: |
| 1000 | False | comment | 81920 | 40960 | 155648 |
| 1000 | False | comment_closure | 286720 | 204800 | 516096 |
| 1000 | False | comment_ns | 49152 | 57344 | 131072 |
| 1000 | False | comment_path | 98304 | 40960 | 172032 |
| 1000 | False | friendship | 229376 | 172032 | 425984 |
| 1000 | True | comment | 81920 | 73728 | 188416 |
| 1000 | True | comment_closure | 286720 | 589824 | 901120 |
| 1000 | True | comment_ns | 49152 | 106496 | 180224 |
| 1000 | True | comment_path | 98304 | 212992 | 344064 |
| 1000 | True | friendship | 229376 | 303104 | 557056 |
