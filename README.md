# deconz-to-mqtt

A simple python bridge between DeCONZ (Phoscon Webapp) and MQTT brokers.

Propagates websocket events from DeCONZ to the MQTT bus. Enriches them with
information gathered by the DeCONZ REST API if applicable. Custom mapping of
topics and message content, if you dare to edit python source code (topics.py)


# Installation

You need Python 3.7.

You need several libraries for the code to work:

```pip install aiohttp websockets aiomqtt```

Clone this repository into ```/opt```:

```
cd /opt
sudo git clone https://github.com/oxytu/deconz-to-mqtt/
```

Don't forget to copy and adopt the configuration file (see below)

Copy ```deconz-to-mqtt.service``` to ```/lib/systemd/system/```. Then register the service on your system:

```
sudo systemctl daemon-reload
sudo systemctl enable deconz-to-mqtt
sudo systemctl start deconz-to-mqtt
```

# Configuration

Copy the file ```config.yml.dist``` to ```config.yml``` and edit to match your
configuration. Don't forget to create an API key in your DeCONZ installation
and to insert it at the right place.


# Startup

Simply run ```python3 server.py```
