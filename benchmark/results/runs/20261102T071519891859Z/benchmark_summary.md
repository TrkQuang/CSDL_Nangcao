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
| Adjacency List | No | 2.743 | 0.221 | 63.000 | 0.000 |
| Adjacency List | Yes | 2.269 | 0.183 | 63.000 | 0.000 |
| Path Enumeration | No | 0.710 | 0.121 | 15.000 | 0.000 |
| Path Enumeration | Yes | 0.311 | 0.158 | 19.000 | 0.000 |
| Nested Set | No | 0.889 | 0.159 | 9.000 | 0.000 |
| Nested Set | Yes | 0.131 | 0.122 | 12.000 | 0.000 |
| Closure Table | No | 0.161 | 0.065 | 10.000 | 0.000 |
| Closure Table | Yes | 0.087 | 0.056 | 12.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 22.961 | 0.153 | 849.000 | 0.000 |
| Adjacency List | Yes | 7.178 | 0.178 | 8047.000 | 0.000 |
| Path Enumeration | No | 4.286 | 0.115 | 142.000 | 0.000 |
| Path Enumeration | Yes | 1.312 | 0.111 | 141.000 | 0.000 |
| Nested Set | No | 5.917 | 0.113 | 58.000 | 0.000 |
| Nested Set | Yes | 0.916 | 0.132 | 73.000 | 0.000 |
| Closure Table | No | 1.225 | 0.081 | 42.000 | 0.000 |
| Closure Table | Yes | 0.535 | 0.048 | 42.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 258.456 | 0.159 | 10288.000 | 0.000 |
| Adjacency List | Yes | 102.242 | 0.263 | 95810.000 | 0.000 |
| Path Enumeration | No | 44.134 | 0.127 | 1607.000 | 0.000 |
| Path Enumeration | Yes | 14.178 | 0.112 | 1877.000 | 0.000 |
| Nested Set | No | 42.146 | 0.118 | 544.000 | 0.000 |
| Nested Set | Yes | 11.489 | 0.147 | 499.000 | 0.000 |
| Closure Table | No | 7.249 | 0.056 | 435.000 | 0.000 |
| Closure Table | Yes | 7.405 | 0.073 | 394.000 | 0.000 |

## INSERT_Leaf

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.270 | 0.007 | 26.000 | 0.000 |
| Adjacency List | Yes | 0.201 | 0.010 | 28.000 | 0.000 |
| Path Enumeration | No | 0.620 | 0.015 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.241 | 0.008 | 46.000 | 0.000 |
| Nested Set | No | 19.331 | 0.008 | 19582.000 | 0.000 |
| Nested Set | Yes | 35.008 | 0.018 | 22441.000 | 0.000 |
| Closure Table | No | 0.685 | 0.006 | 100.000 | 0.000 |
| Closure Table | Yes | 0.300 | 0.009 | 83.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.556 | 0.014 | 26.000 | 0.000 |
| Adjacency List | Yes | 0.399 | 0.020 | 28.000 | 0.000 |
| Path Enumeration | No | 0.269 | 0.006 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.313 | 0.008 | 48.000 | 0.000 |
| Nested Set | No | 330.704 | 0.015 | 228525.000 | 0.000 |
| Nested Set | Yes | 341.841 | 0.015 | 421954.000 | 0.000 |
| Closure Table | No | 6.519 | 0.013 | 526.000 | 0.000 |
| Closure Table | Yes | 0.448 | 0.008 | 87.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.318 | 0.007 | 25.000 | 0.000 |
| Adjacency List | Yes | 0.137 | 0.006 | 28.000 | 0.000 |
| Path Enumeration | No | 0.284 | 0.007 | 40.000 | 0.000 |
| Path Enumeration | Yes | 0.421 | 0.010 | 49.000 | 0.000 |
| Nested Set | No | 2785.442 | 0.008 | 2200148.000 | 0.000 |
| Nested Set | Yes | 3725.398 | 0.014 | 3940715.000 | 26653.000 |
| Closure Table | No | 167.845 | 0.014 | 550.000 | 5288.000 |
| Closure Table | Yes | 0.228 | 0.007 | 89.000 | 0.000 |

## UPDATE_MoveLeaf

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.301 | 0.006 | 32.000 | 0.000 |
| Adjacency List | Yes | 0.215 | 0.008 | 38.000 | 0.000 |
| Path Enumeration | No | 0.726 | 0.014 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.309 | 0.009 | 55.000 | 0.000 |
| Nested Set | No | 22.788 | 0.009 | 21833.000 | 0.000 |
| Nested Set | Yes | 27.223 | 0.012 | 25871.000 | 0.000 |
| Closure Table | No | 1.427 | 0.006 | 139.000 | 0.000 |
| Closure Table | Yes | 0.340 | 0.009 | 98.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 1.165 | 0.011 | 116.000 | 0.000 |
| Adjacency List | Yes | 0.300 | 0.011 | 49.000 | 0.000 |
| Path Enumeration | No | 1.240 | 0.008 | 125.000 | 0.000 |
| Path Enumeration | Yes | 0.247 | 0.006 | 70.000 | 0.000 |
| Nested Set | No | 892.460 | 0.008 | 938775.000 | 0.000 |
| Nested Set | Yes | 1165.895 | 0.019 | 1084281.000 | 0.000 |
| Closure Table | No | 20.651 | 0.013 | 1077.000 | 0.000 |
| Closure Table | Yes | 0.255 | 0.006 | 116.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 9.329 | 0.008 | 957.000 | 0.000 |
| Adjacency List | Yes | 0.673 | 0.008 | 231.000 | 0.000 |
| Path Enumeration | No | 11.938 | 0.008 | 966.000 | 0.000 |
| Path Enumeration | Yes | 0.743 | 0.008 | 251.000 | 0.000 |
| Nested Set | No | 8183.649 | 0.013 | 8483466.000 | 0.000 |
| Nested Set | Yes | 10343.559 | 0.015 | 9948788.000 | 103261.000 |
| Closure Table | No | 381.443 | 0.015 | 3361.000 | 9184.000 |
| Closure Table | Yes | 0.934 | 0.013 | 303.000 | 0.000 |

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
| 100000 | True | comment_path | 13139968 | 26550272 | 39723008 |
| 100000 | True | friendship | 22142976 | 26992640 | 49160192 |
