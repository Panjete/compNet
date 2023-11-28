# compNet

## TCP NewRenoPlus

- Housed in `newrenoplus/` is the Experimentation and Analysis of current TCP Congestion Control Protocols (CCPs) - Vegas, Reno, Westwood and Cubic.
- Simulation was performed on the `ns3-29` software.
- The Congestion Window plots, the log files and packet captures for all the variations of experiments (varying Channel Rates, Application Rates) are stashed in the `results/` subdirectory.

- To run, execute `run.sh`, which handles all parameter selection and topology selection.


- Add `TcpNewRenoPlus.cc` and `TcpNewRenoPlus.h` to `ns3`'s TCP files to use it for Congestion Control.

- `tcp_protocols.pdf` presents the complete analysis on the performance of these protocols.

## Peer-Server-Peer Distribution Mechanism

- Code housed in `PSP` directory.
- An attempt at obtaining the best-of-both-worlds benefits from P2P and a fully Client-Server File sharing.
- Objective : File sharing between nodes, node queryies caches for file, if not in cache then request forwarded to other nodes. 

- A Cache, housed in `lrupart[12].py` is used to aid the distribution as well.
- We experiment with using TCP and UDP for the Data and Control Planes, as well as the optimum Caching required.
- A complete Analysis of performance is done in `analysis.pdf`.

