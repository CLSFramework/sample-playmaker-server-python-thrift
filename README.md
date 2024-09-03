# Sample Playmaker Server (Python - Thrift)

This repository contains a sample Playmaker server written in Python using Thrift, designed to facilitate the development of a Soccer Simulation 2D team.

Traditionally, teams in the Soccer Simulation 2D league are implemented in C++ using existing base codes. Each agent in the team receives observations from the Soccer Simulation 2D server and sends actions back to it. However, with the Cross Language Soccer Framework (CLSF), we have enhanced the Helios base code to interact with a Thrift/gRPC server. This server-based approach allows the simulation to send the necessary information for decision-making to a server and receive the corresponding actions, which are then communicated back to the Soccer Simulation 2D server.

This flexibility enables you to develop your team in any programming language of your choice, breaking the constraints of C++.

This repository provides a sample server implemented in Python using Thrift. You can use this server as a starting point to develop and customize your own team.

To learn more about the Cross Language Soccer Framework, visit the [official repository](https://github.com/CLSFramework/cross-language-soccer-framework/wiki)

![image](https://github.com/user-attachments/assets/0c22d0e5-a1ad-4a43-8cba-a9fc70c6ed5b)

![image](https://github.com/Cross-Language-Soccer-Framework/cross-language-soccer-framework/assets/25696836/7b0b1d49-7001-479c-889f-46a96a8802c4)

![image](https://github.com/user-attachments/assets/b4484095-0913-4434-bf1f-35f11e8bf629)

![image](https://github.com/user-attachments/assets/bc1b9c86-f772-4df8-a420-438e363c59b5)

## Preparation

To run a Soccer Simulation 2D game using the CLSF, you need to have RCSSServer, SoccerSimulationProxy, and Monitor to visualize the game.

### RCSSServer
To download the latest AppImage of the RCSSServer,  you can run the following command:

```bash
cd scripts
./download-rcssserver.sh
```

Note: You can build the RCSSServer from the source code. For more information, visit the [official repository](https://github.com/rcsoccersim/rcssserver).

To run the RCSSServer AppImage, you need to install FUSE. You can install it by running the following command:

```bash
sudo apt-get install fuse
```

### SoccerSimulationProxy

To download the latest AppImage of the SoccerSimulationProxy, you can run the following command:

```bash
cd scripts
./download-proxy.sh
```

Note: You can build the SoccerSimulationProxy from the source code. For more information, visit the [official repository](https://github.com/CLSFramework/soccer-simulation-proxy)

To run the SoccerSimulationProxy AppImage, you need to install FUSE. You can install it by running the following command:

```bash
sudo apt-get install fuse
```

### Monitor

To download the latest AppImage of the Monitor, you can download it from the [official repository](https://github.com/rcsoccersim/rcssmonitor/releases).

### Create Python Virtual Environment and Install Dependencies

To create a Python virtual environment and install the dependencies, you can run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running a game

To run a game, you need to run the RCSSServer, Monitor, and then the SoccerSimulationProxy and the sample server.

### Running the RCSSServer
if you have downloaded the RCSSServer AppImage, you can run it by running the following command:

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

### Using start-team.py (This script can be used in Linux)

Note: To use this script you need to download the proxy by using `scripts/download-proxy.sh`.

First, you need to run the RCSSServer, then run the `start-team.py` script:

```bash
python start-team.py
```

You can pass the following arguments to the script:
- `--team-name`: The name of the team (default: `CLSF`)
- `--rpc-port`: The port number for the RPC server (default: `50051`)

### Using start-team.sh (This script can be used in Linux)

Note: To use this script you need to download the proxy by using `scripts/download-proxy.sh`.

First, you need to run the RCSSServer, then run the `start-team.sh` script:

```bash
./start-team.sh
```

You can pass the following arguments to the script:
- `--team-name`: The name of the team (default: `CLSF`)
- `--rpc-port`: The port number for the RPC server (default: `50051`)

### Running the server and client separately (This method can be used in Windows and Linux, but the proxy can only be run in Linux)

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

#### Running the playmaker server in Windows
If you want to run the playmaker server in Windows, you need to somehow connect the proxy to the playmaker server. You can find ip of your local machine(Windows) and use it in the proxy.
