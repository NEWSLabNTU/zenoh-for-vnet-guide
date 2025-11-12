# Starter Experiment

## Network Topology

The baseline is two computers directly connected with 2.5Gbps Ethernet.

The experiments' topology is almost the same as [README](README.md), except the Wired connections are at 2.5Gbps.

## Configuration Files

Same as [README](README.md), except the experiment without SAE.

## Experiments
### iPerf3
#### Client
```
iperf3 -c <IP> -4 -f M -i <INTERVAL> -t 180
```
#### Server
```
iperf3 -s -B <IP> -4
```
#### #1. Baseline Test (Ideal Condition)
- Two PCs were directly connected with 2.5Gbps Ethernet.
- Set the INTERVAL = 1.

#### #2. BPI-to-BPI Test (Initial Setup)
- Set the INTERVAL = 1.

#### #3. Longer Report Interval (i=10)
- Set the INTERVAL = 10.

#### #4. No Periodic Reporting (i=0)
- Set the INTERVAL = 0.

#### #5. Thermal Impact Test (Repeat #2 and #3)
- Due to the observation of high temparatures on the BPIs, we repeated the tests to evaluate thermal effects.
- Test #3 was executed immediately after the test #2 was completed.

#### #6. SAE Disabled Test
- To evaluate whether authentication overhead affected throughput.
- Set the INTERVAL = 10.

## Results

### Bitrates
![iPerf3Experiments](iPerf3Bitrates.svg)
| Max  | Min  | Mean |      Note        |
|------|------|------|------------------|
| 2.35 | 2.26 | 2.35 | 2.5Gbps Wired    |
| 1.61 | 0.60 | 0.96 | Wireless i=1 #1  |
| 1.83 | 0.74 | 1.42 | Wireless i=10 #1 |
| 1.79 | 0.64 | 1.27 | Wireless i=0     |
| 1.48 | 0.59 | 1.04 | Wireless i=1 #2  |
| 1.66 | 0.56 | 1.04 | Wireless i=10 #2 |
| 1.65 | 0.18 | 0.86 | Wireless w/o SAE |

#### Notes
- In a previous test, we increased the number of threads (using -P 4) to check whether the bottleneck was caused by the CPU. The throughput improved by about 1.2×, but still did not reach the ideal performance. Therefore, we assume that there are two levels of bottleneck — one from the CPU and another from the hardware.

- By Jerry's advice, we have tried to check if the electromagnetic shielding affect the result during the experiment of testing wireless without SAE.
However, it is possible that the long interval (10s) has buffered the impact. We cannot observe the corresponding response of shielding.


## Conclusions
- The initial increase in speed for i=10 and i=0 is quite confusing, it may cause by the reduction of CPU overhead from iperf3’s reporting mechanism.

- Test #5 confirmed that thermal throttling further degrades performance.

- Disabling encryption did not improve throughput.
