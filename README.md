# Sample Python Playmaker Server - Thrift

This repository contains a sample Playmaker server written in Python using Thrift, designed to facilitate the development of a Soccer Simulation 2D team.

Traditionally, teams in the Soccer Simulation 2D league are implemented in C++ using existing base codes. Each agent in the team receives observations from the Soccer Simulation 2D server and sends actions back to it. However, with the Cross Language Soccer Framework (CLSF), we have enhanced the Helios base code([SoccerSimulationProxy](https://github.com/CLSFramework/soccer-simulation-proxy)) to interact with a Thrift/gRPC server(PlaymakerServer). 

This server-based approach allows the simulation to send the necessary information for decision-making to a rpc server and receive the corresponding actions, which are then communicated back to the Soccer Simulation 2D server.

This flexibility enables you to develop your team in any programming language of your choice, breaking the constraints of C++.

This repository provides a sample server implemented in Python using Thrift. You can use this server as a starting point to develop and customize your own team.

Also, you can find some scripts to download the RCSSServer, SoccerSimulationProxy, and run the sample server and proxy. To use this framework, you need to have Ubuntu or WSL.

To learn more about the Cross Language Soccer Framework, visit the [official repository](https://github.com/CLSFramework/cross-language-soccer-framework/wiki)

![cls](https://github.com/user-attachments/assets/4daee216-1479-4acd-88f2-9e772b8c7837)

## Preparation

To run a Soccer Simulation 2D game using the CLSF, you need to have RCSSServer, SoccerSimulationProxy, and Monitor to visualize the game.

### RCSSServer
To download the latest AppImage of the RCSSServer,  you can run the following command:

```bash
cd scripts
./download-rcssserver.sh
```

To run the RCSSServer AppImage, you need to install FUSE. You can install it by running the following command:

```bash
sudo apt-get install fuse
```

<u>Notes:</u>
- You can build the RCSSServer from the source code. For more information, visit the [official repository](https://github.com/rcsoccersim/rcssserver).
- The RCSSServer should be run on <u>Linux (preferably Ubuntu) or WSL</u>.



### SoccerSimulationProxy

To download the latest AppImage of the SoccerSimulationProxy, you can run the following command:

```bash
cd scripts
./download-proxy.sh
```

To run the SoccerSimulationProxy AppImage, you need to install FUSE. You can install it by running the following command:

```bash
sudo apt-get install fuse
```

<u>Notes:</u>
- You can build the SoccerSimulationProxy from the source code. For more information, visit the [official repository](https://github.com/CLSFramework/soccer-simulation-proxy)
- The SoccerSimulationProxy should be run on <u>Linux (preferably Ubuntu) or WSL</u>.

### Monitor

To download the latest AppImage of the Monitor, you can download it from the [official repository](https://github.com/rcsoccersim/rcssmonitor/releases).

To run the monitor, you need to install FUSE. You can install it by running the following command:

```bash
sudo apt-get install fuse
```

### Create Python Virtual Environment and Install Dependencies

To create a Python virtual environment and install the dependencies, you can run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./generate.sh # To generate thrift python files
```

## Running a game

To run a game, you need to run the RCSSServer and then the SoccerSimulationProxy and the sample server. To visualize the game, you can run the Monitor.

### Running the RCSSServer
If you have downloaded the RCSSServer AppImage, you can run it by running the following command:

```bash
cd scripts/rcssserver
./rcssserver
```

Otherwise, you built and install the RCSSServer from the source code, you can run the server by running the following command:

```bash
rcssserver
```

## Running the Sample Server and Proxy

There are three different ways to run the sample server:

- Using start-team.py
- Using start-team.sh
- Running the server and client separately

### Using start-team.py (This script can be used in Ubuntu or WSL)

Note: To use this script you need to download the proxy by using `scripts/download-proxy.sh`.

Run the `start-team.py` script:

```bash
python start-team.py
```

You can pass the following arguments to the script:
- `--team-name`: The name of the team (default: `CLSF`)
- `--rpc-port`: The port number for the RPC server (default: `50051`)

### Using start-team.sh (This script can be used in Linux)

Note: To use this script you need to download the proxy by using `scripts/download-proxy.sh`.

Run the `start-team.sh` script:

```bash
./start-team.sh
```

You can pass the following arguments to the script:
- `--team-name`: The name of the team (default: `CLSF`)
- `--rpc-port`: The port number for the RPC server (default: `50051`)

### Running the server and client separately 

(This method can be used in Windows and Linux, but the proxy can only be run in Linux)

To run the server, you can run the following command:

```bash
python server.py
```

You can pass the following arguments to the server:
- `--rpc-port`: The port number for the RPC server (default: `50051`)

If you want to run the proxy agents, you can run the following command:

```bash
cd scripts/proxy
./start.sh
```

To learn more about the Soccer Simulation Proxy, arguments you can pass, and how to run it, build it from source, visit the [official repository](https://github.com/CLSFramework/soccer-simulation-proxy)

#### Running the playmaker server in Windows (Not recommended)
If you want to run the playmaker server in Windows, you need to somehow connect the proxy to the playmaker server. You can find ip of your local machine(Windows) and use it in the proxy.
<u>Right now due to some issues with Python multiprocessing, the playmaker server can't be run in Windows.</u>

## How does it work?
Berifly, the Soccer Simulation 2D server sends the observations to the proxy, which forwards them to the playmaker server. The playmaker server processes the observations and sends the actions back to the proxy, which forwards them to the Soccer Simulation 2D server.

## Citation

- [Cross Language Soccer Framework](https://arxiv.org/pdf/2406.05621)
- Zare, N., Sayareh, A., Sadraii, A., Firouzkouhi, A. and Soares, A., 2024. Cross Language Soccer Framework: An Open Source Framework for the RoboCup 2D Soccer Simulation. arXiv preprint arXiv:2406.05621.
