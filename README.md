# TCP-UDP Video Serve Simulation

[![GitHub repo size](https://img.shields.io/github/repo-size/nuhyurdev/tcp-udp-video-serve-simulation)](https://github.com/nuhyurdev/tcp-udp-video-serve-simulation)
[![GitHub last commit](https://img.shields.io/github/last-commit/nuhyurdev/tcp-udp-video-serve-simulation)](https://github.com/nuhyurdev/tcp-udp-video-serve-simulation)
[![GitHub issues](https://img.shields.io/github/issues/nuhyurdev/tcp-udp-video-serve-simulation)](https://github.com/nuhyurdev/tcp-udp-video-serve-simulation)
[![GitHub license](https://img.shields.io/github/license/nuhyurdev/tcp-udp-video-serve-simulation)](https://github.com/nuhyurdev/tcp-udp-video-serve-simulation)

## Overview

This project demonstrates a video serving simulation using both TCP and UDP protocols. It provides insights into the differences between these protocols in the context of video streaming.

## Features

- **TCP Video Streaming:** Simulates video transmission over the Transmission Control Protocol (TCP), ensuring reliable data delivery.
- **UDP Video Streaming:** Simulates video transmission over the User Datagram Protocol (UDP), offering faster delivery with potential data loss.

## Prerequisites

- Python 3.x
- Required Python libraries (detailed in `requirements.txt`)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nuhyurdev/tcp-udp-video-serve-simulation.git
   ```


2. **Navigate to the project directory:**
   ```bash
   cd tcp-udp-video-serve-simulation
   ```


3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```


## Usage

1. **Running the TCP server:**
   ```bash
   python src/tcp_server.py
   ```


2. **Running the UDP server:**
   ```bash
   python src/udp_server.py
   ```


3. **Running the client:**
   ```bash
   python src/client.py
   ```


Ensure that the server is running before starting the client. Modify the server and client configurations as needed in the respective Python scripts.

## Demonstration Videos

The following videos illustrate the simulation of video serving over TCP and UDP:

### TCP Video Simulation

![TCP Video Simulation](tcp.mp4)

### UDP Video Simulation

![UDP Video Simulation](udp.mp4)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For more information and updates, visit the [GitHub repository](https://github.com/nuhyurdev/tcp-udp-video-serve-simulation). 