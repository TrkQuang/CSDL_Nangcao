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
| Adjacency List | No | 1.474 | 0.121 | 63.000 | 0.000 |
| Adjacency List | Yes | 3.085 | 0.391 | 63.000 | 0.000 |
| Path Enumeration | No | 0.245 | 0.053 | 15.000 | 0.000 |
| Path Enumeration | Yes | 0.543 | 0.290 | 19.000 | 0.000 |
| Nested Set | No | 0.316 | 0.078 | 9.000 | 0.000 |
| Nested Set | Yes | 0.197 | 0.182 | 12.000 | 0.000 |
| Closure Table | No | 0.081 | 0.038 | 10.000 | 0.000 |
| Closure Table | Yes | 0.126 | 0.078 | 12.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 17.089 | 0.145 | 849.000 | 0.000 |
| Adjacency List | Yes | 7.223 | 0.149 | 8047.000 | 0.000 |
| Path Enumeration | No | 2.210 | 0.068 | 142.000 | 0.000 |
| Path Enumeration | Yes | 1.268 | 0.095 | 140.000 | 0.000 |
| Nested Set | No | 2.866 | 0.087 | 58.000 | 0.000 |
| Nested Set | Yes | 0.902 | 0.125 | 73.000 | 0.000 |
| Closure Table | No | 0.532 | 0.038 | 42.000 | 0.000 |
| Closure Table | Yes | 0.527 | 0.054 | 42.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 233.665 | 0.164 | 10288.000 | 0.000 |
| Adjacency List | Yes | 90.894 | 0.191 | 95810.000 | 0.000 |
| Path Enumeration | No | 48.384 | 0.098 | 1607.000 | 0.000 |
| Path Enumeration | Yes | 15.048 | 0.135 | 1852.000 | 0.000 |
| Nested Set | No | 59.007 | 0.138 | 544.000 | 0.000 |
| Nested Set | Yes | 13.517 | 0.163 | 499.000 | 0.000 |
| Closure Table | No | 7.658 | 0.069 | 435.000 | 0.000 |
| Closure Table | Yes | 8.841 | 0.086 | 394.000 | 0.000 |

## INSERT_Leaf

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.513 | 0.009 | 26.000 | 0.000 |
| Adjacency List | Yes | 0.135 | 0.005 | 28.000 | 0.000 |
| Path Enumeration | No | 0.452 | 0.011 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.182 | 0.005 | 46.000 | 0.000 |
| Nested Set | No | 22.382 | 0.011 | 19582.000 | 0.000 |
| Nested Set | Yes | 22.666 | 0.012 | 22441.000 | 0.000 |
| Closure Table | No | 1.582 | 0.013 | 100.000 | 0.000 |
| Closure Table | Yes | 0.219 | 0.007 | 83.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.363 | 0.009 | 26.000 | 0.000 |
| Adjacency List | Yes | 0.147 | 0.006 | 28.000 | 0.000 |
| Path Enumeration | No | 0.324 | 0.006 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.245 | 0.007 | 48.000 | 0.000 |
| Nested Set | No | 321.481 | 0.008 | 228525.000 | 0.000 |
| Nested Set | Yes | 322.535 | 0.013 | 421954.000 | 0.000 |
| Closure Table | No | 13.250 | 0.017 | 526.000 | 0.000 |
| Closure Table | Yes | 0.230 | 0.007 | 87.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.304 | 0.007 | 26.000 | 0.000 |
| Adjacency List | Yes | 0.182 | 0.007 | 28.000 | 0.000 |
| Path Enumeration | No | 0.293 | 0.007 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.213 | 0.007 | 49.000 | 0.000 |
| Nested Set | No | 2880.428 | 0.008 | 2200149.000 | 0.000 |
| Nested Set | Yes | 3403.259 | 0.013 | 3939864.000 | 27504.000 |
| Closure Table | No | 127.713 | 0.014 | 550.000 | 5288.000 |
| Closure Table | Yes | 0.301 | 0.011 | 89.000 | 0.000 |

## UPDATE_MoveLeaf

Generated from actual rows in `benchmark_results.csv`.
Each value is median of recorded repeats. Empty CSV produces no result.

### Dataset 1,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 0.479 | 0.010 | 32.000 | 0.000 |
| Adjacency List | Yes | 0.183 | 0.006 | 38.000 | 0.000 |
| Path Enumeration | No | 0.585 | 0.011 | 41.000 | 0.000 |
| Path Enumeration | Yes | 0.243 | 0.006 | 55.000 | 0.000 |
| Nested Set | No | 36.897 | 0.010 | 21833.000 | 0.000 |
| Nested Set | Yes | 25.407 | 0.013 | 25871.000 | 0.000 |
| Closure Table | No | 3.233 | 0.013 | 139.000 | 0.000 |
| Closure Table | Yes | 0.297 | 0.007 | 98.000 | 0.000 |

### Dataset 10,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 1.813 | 0.012 | 116.000 | 0.000 |
| Adjacency List | Yes | 0.160 | 0.006 | 49.000 | 0.000 |
| Path Enumeration | No | 1.739 | 0.007 | 125.000 | 0.000 |
| Path Enumeration | Yes | 0.223 | 0.007 | 70.000 | 0.000 |
| Nested Set | No | 950.372 | 0.008 | 938775.000 | 0.000 |
| Nested Set | Yes | 933.786 | 0.013 | 1084281.000 | 0.000 |
| Closure Table | No | 18.589 | 0.008 | 1077.000 | 0.000 |
| Closure Table | Yes | 0.339 | 0.010 | 116.000 | 0.000 |

### Dataset 100,000 nodes

| Model | Index | Execution ms | Planning ms | Hit blocks | Read blocks |
| --- | --- | ---: | ---: | ---: | ---: |
| Adjacency List | No | 14.347 | 0.008 | 957.000 | 0.000 |
| Adjacency List | Yes | 0.880 | 0.007 | 231.000 | 0.000 |
| Path Enumeration | No | 14.712 | 0.008 | 966.000 | 0.000 |
| Path Enumeration | Yes | 1.100 | 0.007 | 251.000 | 0.000 |
| Nested Set | No | 8036.136 | 0.009 | 8483466.000 | 0.000 |
| Nested Set | Yes | 10148.457 | 0.014 | 9948522.000 | 103308.000 |
| Closure Table | No | 267.488 | 0.013 | 3311.000 | 9234.000 |
| Closure Table | Yes | 1.144 | 0.008 | 303.000 | 0.000 |

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
| 10000 | True | comment_path | 1138688 | 2310144 | 3481600 |
| 10000 | True | friendship | 2220032 | 2727936 | 4972544 |
| 100000 | False | comment | 7659520 | 2260992 | 9953280 |
| 100000 | False | comment_closure | 47259648 | 38289408 | 85581824 |
| 100000 | False | comment_ns | 4431872 | 3047424 | 7503872 |
| 100000 | False | comment_path | 13139968 | 2260992 | 15433728 |
| 100000 | False | friendship | 22142976 | 15736832 | 37904384 |
| 100000 | True | comment | 7659520 | 3915776 | 11608064 |
| 100000 | True | comment_closure | 47259648 | 95961088 | 143253504 |
| 100000 | True | comment_ns | 4431872 | 6225920 | 10682368 |
| 100000 | True | comment_path | 13139968 | 26419200 | 39591936 |
| 100000 | True | friendship | 22142976 | 26992640 | 49160192 |
