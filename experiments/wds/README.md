# WDS Experiment

This experiment is composed of **two BPIs** connected wirelessly via Wireless Distribution System (**WDS**) and aims to measure basic **throughtput** and **latency** for TCP connection via **iperf3**, **netperf3**, **z_ping**. 

## Objectives
1) measure maximum **throughput** that the devices are capable off with no traffic and optimized for best performance
2) measure the minimum **latency** that the devices can achieve with not traffic
3) execute the benchmark using [i|net]perf3 tool **without Zenoh** running and **with Zenoh** for comparison 

## Network Topology

The experiment include two computer which one is a *Client* and the second is *Server*. Then two devices BPI-A and BPI-B. The computers as connected via Ethernet cable to the each BPI and a wireless connection is established between the BPIs (i.e., WDS).

![network_topology](wds_network_topology.svg)

**Pre-Conditions**
- Be sure that you can communicate with the all devices on the network, e.g., by using ping. 
- Verify if Zenoh service is OFF or ON on all BPI devices before running the corresponding benchmark.
- Check if you have the correct date on all BPIs. If not, check the configuration at [Using NTP]().

**Zenoh**
 ZClient <-> ZRouter <-> ZRouter <-> ZClient
- Client and Server as Zenoh Client
- BPI-[A | B] as Zenoh Router


**WDS Configuration**
- IEEE 802.11ax (WiFi 6)
- Radio frequency 5 GHz
- Channel 100
- Channel width 160 MHz
- Security WPA3 SAE
- BPI-A includes DHCP server

## Configuration files

List of configuration files included in the folder and the path where the config must be placed on the BPI.

BPI-A:
- network -> /etc/config/network
- wireless -> /etc/config/wireless
- dhcp -> /etc/config/dhcp
- zenohd.yaml -> /etc/config/zenohd.yaml

BPI-B:
- network -> /etc/config/network
- wireless -> /etc/config/wireless
- dhcp -> /etc/config/dhcp
- zenohd.yaml -> /etc/config/zenohd.yaml


## Results

### iperf3

#### Client
``
iperf3 -c <IP> -f M -i 1 -t 180
``

#### Server
```
systemctl iperf3 start
```

#### Throughtput

| Interval | Transfer | Bitrate |
| -------- | -------- | -------- |
| 0.00-180.00 sec     | 19.1 GBytes     | 109 MBytes/sec     |


![bandwidth_iperf](https://hackmd.io/_uploads/SyP5SkmKkl.svg =500x)


### netperf

#### Client
```
netperf -t omni -H 192.168.1.160 -l 180 -- -r 1048576,1024   \  
    -O MIN_LATENCY,MEAN_LATENCY,MAX_LATENCY,TRANSACTION_RATE
```

#### Server
```
systemctl netperf start
```

#### Latency

##### Road Trip Time 1MB/1MB

| Interval | Request payload | Response payload
| -------- | -------- | -------- |
| 180 s | 1048576 Bytes | 1048576 Bytes |

| Min. Latency      |  Avg. Latency      |  Max. Latency      | Trans. Rate Tran/s      
| -------- | -------- | -------- | -------- |
| 20.895 ms   | 24.680 ms     | 72.161 ms        | 40.516 Trans/s



##### Road Trip Time 1MB/1KB
| Interval | Request payload | Response payload
| -------- | -------- | -------- |
| 180 s | 1048576 Bytes  | 1024 Bytes |

| Min. Latency      |  Avg. Latency      |  Max. Latency      | Trans. Rate Tran/s      
| -------- | -------- | -------- | -------- |
| 10.837 ms   | 14.176 ms     | 31.576 ms        | 70.532 Trans/s


##### Road Trip Time 1KB/1KB

| Interval | Request payload | Response payload
| -------- | -------- | -------- |
| 180 s | 1024 Bytes | 1024 Bytes |

| Min. Latency      |  Avg. Latency      |  Max. Latency      | Trans. Rate Tran/s      
| -------- | -------- | -------- | -------- |
| 0.840 ms   | 1.700 ms     | 12.385 ms        | 588.009 Trans/s


### zenoh

**Client**
```
./z_ping --mode client --connect tcp/192.168.1.2:7447 \
    --warmup 5 --no-multicast-scouting --samples 55000 1048576
```

**Server**
```
./z_pong --mode client --connect tcp/192.168.1.1:7447
```

##### Road Trip Time 1KB/1KB

| Interval | Request payload | Response payload
| -------- | -------- | -------- |
| 176.14 s | 1024 Bytes | 1024 Bytes |

| Min. Latency      |  Avg. Latency      |  Max. Latency
| -------- | -------- | -------- |
| 1.097 ms   | 1.677 ms     | 12.695 ms 


##### Road Trip Time 1MB/1MB

| Interval | Request payload | Response payload
| -------- | -------- | -------- |
| 203.528 s | 1048576 Bytes | 1048576 Bytes |

| Min. Latency      |  Avg. Latency      |  Max. Latency
| -------- | -------- | -------- |
| 38.132 ms   | 40.705 ms     | 78.449 ms


### zenoh (no-express)


**Client**
```
./z_ping --mode client --connect tcp/192.168.1.2:7447 \
    --warmup 5 --no-multicast-scouting --samples 3400 --no-express 1048576
```

**Server**
```
./z_pong --mode client --connect tcp/192.168.1.1:7447 --no-express
```

##### Road Trip Time 1MB/1MB

| Interval | Request payload | Response payload
| -------- | -------- | -------- |
| 191.121 s | 1048576 Bytes | 1048576 Bytes |

| Min. Latency      |  Avg. Latency      |  Max. Latency
| -------- | -------- | -------- |
| 52.010 ms   | 56.212 ms     | 492.311 ms
