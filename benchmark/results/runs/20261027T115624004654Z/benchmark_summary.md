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
| Adjacency List | No | 1.461 | 0.114 | 63.000 | 0.000 |
| Adjacency List | Yes | 1.235 | 0.132 | 63.000 | 0.000 |
| Path Enumeration | No | 0.502 | 0.076 | 15.000 | 0.000 |
| Path Enumeration | Yes | 0.131 | 0.081 | 19.000 | 0.000 |
| Nested Set | No | 0.317 | 0.070 | 9.000 | 0.000 |
| Nested Set | Yes | 0.160 | 0.133 | 12.000 | 0.000 |
| Closure Table | No | 0.103 | 0.046 | 10.000 | 0.000 |
| Closure Table | Yes | 0.091 | 0.050 | 12.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 17.052 | 0.133 | 849.000 | 0.000 |
| Adjacency List | Yes | 5.901 | 0.132 | 8047.000 | 0.000 |
| Path Enumeration | No | 2.136 | 0.050 | 142.000 | 0.000 |
| Path Enumeration | Yes | 0.913 | 0.081 | 141.000 | 0.000 |
| Nested Set | No | 2.864 | 0.094 | 58.000 | 0.000 |
| Nested Set | Yes | 1.121 | 0.130 | 73.000 | 0.000 |
| Closure Table | No | 0.519 | 0.035 | 42.000 | 0.000 |
| Closure Table | Yes | 0.516 | 0.044 | 42.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 231.705 | 0.152 | 10288.000 | 0.000 |
| Adjacency List | Yes | 85.509 | 0.185 | 95810.000 | 0.000 |
| Path Enumeration | No | 36.880 | 0.098 | 1607.000 | 0.000 |
| Path Enumeration | Yes | 13.381 | 0.130 | 1858.000 | 0.000 |
| Nested Set | No | 52.214 | 0.122 | 544.000 | 0.000 |
| Nested Set | Yes | 13.147 | 0.152 | 499.000 | 0.000 |
| Closure Table | No | 7.148 | 0.056 | 435.000 | 0.000 |
| Closure Table | Yes | 6.814 | 0.071 | 394.000 | 0.000 |

## INSERT_Leaf

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.298 | 0.007 | 26.000 | 0.000 |
| Adjacency List | Yes | 0.157 | 0.007 | 28.000 | 0.000 |
| Path Enumeration | No | 0.291 | 0.006 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.216 | 0.007 | 46.000 | 0.000 |
| Nested Set | No | 20.560 | 0.007 | 19582.000 | 0.000 |
| Nested Set | Yes | 22.932 | 0.011 | 22441.000 | 0.000 |
| Closure Table | No | 1.051 | 0.006 | 100.000 | 0.000 |
| Closure Table | Yes | 0.390 | 0.014 | 83.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.252 | 0.006 | 26.000 | 0.000 |
| Adjacency List | Yes | 0.145 | 0.006 | 28.000 | 0.000 |
| Path Enumeration | No | 0.505 | 0.012 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.207 | 0.006 | 48.000 | 0.000 |
| Nested Set | No | 258.811 | 0.007 | 228525.000 | 0.000 |
| Nested Set | Yes | 324.625 | 0.012 | 421954.000 | 0.000 |
| Closure Table | No | 8.618 | 0.013 | 526.000 | 0.000 |
| Closure Table | Yes | 0.359 | 0.006 | 87.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.279 | 0.007 | 25.000 | 0.000 |
| Adjacency List | Yes | 0.197 | 0.010 | 28.000 | 0.000 |
| Path Enumeration | No | 0.275 | 0.006 | 40.000 | 0.000 |
| Path Enumeration | Yes | 0.260 | 0.008 | 49.000 | 0.000 |
| Nested Set | No | 2427.696 | 0.008 | 2200149.000 | 0.000 |
| Nested Set | Yes | 3391.805 | 0.013 | 3940357.000 | 27011.000 |
| Closure Table | No | 142.623 | 0.014 | 550.000 | 5288.000 |
| Closure Table | Yes | 0.490 | 0.008 | 89.000 | 0.000 |

## UPDATE_MoveLeaf

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.425 | 0.007 | 32.000 | 0.000 |
| Adjacency List | Yes | 0.222 | 0.007 | 38.000 | 0.000 |
| Path Enumeration | No | 0.421 | 0.010 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.300 | 0.008 | 55.000 | 0.000 |
| Nested Set | No | 21.769 | 0.010 | 21833.000 | 0.000 |
| Nested Set | Yes | 46.006 | 0.018 | 25871.000 | 0.000 |
| Closure Table | No | 1.581 | 0.006 | 139.000 | 0.000 |
| Closure Table | Yes | 0.673 | 0.013 | 98.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 2.261 | 0.013 | 116.000 | 0.000 |
| Adjacency List | Yes | 0.247 | 0.012 | 49.000 | 0.000 |
| Path Enumeration | No | 1.693 | 0.006 | 125.000 | 0.000 |
| Path Enumeration | Yes | 0.284 | 0.006 | 70.000 | 0.000 |
| Nested Set | No | 837.115 | 0.008 | 938775.000 | 0.000 |
| Nested Set | Yes | 933.816 | 0.013 | 1084281.000 | 0.000 |
| Closure Table | No | 20.177 | 0.026 | 1077.000 | 0.000 |
| Closure Table | Yes | 0.246 | 0.006 | 116.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 13.560 | 0.008 | 957.000 | 0.000 |
| Adjacency List | Yes | 0.684 | 0.008 | 231.000 | 0.000 |
| Path Enumeration | No | 16.477 | 0.008 | 966.000 | 0.000 |
| Path Enumeration | Yes | 0.742 | 0.009 | 251.000 | 0.000 |
| Nested Set | No | 8226.932 | 0.011 | 8483466.000 | 0.000 |
| Nested Set | Yes | 9180.796 | 0.013 | 9948706.000 | 103406.000 |
| Closure Table | No | 352.790 | 0.015 | 3249.000 | 9296.000 |
| Closure Table | Yes | 0.854 | 0.008 | 303.000 | 0.000 |

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
| 10000 | False | comment | 770048 | 245760 | 1048576 |
| 10000 | False | comment_closure | 3776512 | 2949120 | 6750208 |
| 10000 | False | comment_ns | 450560 | 319488 | 794624 |
| 10000 | False | comment_path | 1138688 | 245760 | 1417216 |
| 10000 | False | friendship | 2220032 | 1589248 | 3833856 |
| 10000 | True | comment | 770048 | 425984 | 1228800 |
| 10000 | True | comment_closure | 3776512 | 7585792 | 11386880 |
| 10000 | True | comment_ns | 450560 | 655360 | 1130496 |
| 10000 | True | comment_path | 1138688 | 2301952 | 3473408 |
| 10000 | True | friendship | 2220032 | 2727936 | 4972544 |
| 100000 | False | comment | 7659520 | 2260992 | 9953280 |
| 100000 | False | comment_closure | 47259648 | 38289408 | 85581824 |
| 100000 | False | comment_ns | 4431872 | 3047424 | 7503872 |
| 100000 | False | comment_path | 13139968 | 2260992 | 15433728 |
| 100000 | False | friendship | 22142976 | 15736832 | 37904384 |
| 100000 | True | comment | 7659520 | 3915776 | 11608064 |
| 100000 | True | comment_closure | 47259648 | 95961088 | 143253504 |
| 100000 | True | comment_ns | 4431872 | 6225920 | 10682368 |
| 100000 | True | comment_path | 13139968 | 26370048 | 39542784 |
| 100000 | True | friendship | 22142976 | 26992640 | 49160192 |
