# deconz-to-mqtt

A simple python bridge between DeCONZ (Phoscon Webapp) and MQTT brokers.

Propagates websocket events from DeCONZ to the MQTT bus. Enriches them with
information gathered by the DeCONZ REST API if applicable. Custom mapping of
topics and message content, if you dare to edit python source code (topics.py)


# Installation

You need several libraries for the code to work:

```pip install aiohttp```
```pip install websockets```
```pip install hbmqtt```


# Startup

Simply run ```python3 server.py```
