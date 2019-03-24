#!/usr/bin/env python

import asyncio
import aiohttp
import websockets
import json
import yaml
from hbmqtt.client import MQTTClient, ClientException

from server_lib import topic_generators, message_generators
import topics

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

def mqtt_topic_function(websocket_message, rest_extended_data):
	type = rest_extended_data['type']
	if type in topic_generators:
		return cfg['mqtt']['topic_root'] + topic_generators[type](websocket_message, rest_extended_data)
	else:
		return cfg['mqtt']['topic_root'] + '/'.join(filter(None, [websocket_message['r'], rest_extended_data['type'], rest_extended_data['name']]))

def mqtt_message_function(websocket_message, rest_extended_data):
	type = rest_extended_data['type']
	if type in message_generators:
		return message_generators[type](websocket_message, rest_extended_data)
	else:
		return websocket_message

@asyncio.coroutine
async def rest_fetch(session, url):
	async with session.get(url) as response:
		return await response.text()

@asyncio.coroutine
async def extend_websocket_data(websocket_json):
	async with aiohttp.ClientSession() as session:

		handlers = {
			"sensors": "sensors/" + websocket_json['id'],
			"lights": "lights/" + websocket_json['id'],
			"groups": "groups/" + websocket_json['id'],
		}

		try:
			if websocket_json['r'] in handlers:
				response = await rest_fetch(session, cfg['deconz']['rest_url'] + handlers[websocket_json['r']])
				return json.loads(response)
		except:
			pass
		
		return {}

@asyncio.coroutine
async def receive_deconz_messages():
	async with websockets.connect(cfg['deconz']['websocket_url']) as websocket:

		async for message in websocket:
			mqttc = MQTTClient()
			await mqttc.connect(cfg['mqtt']['url'])

			print(f"<<deconz<< {message}")
			message_json = json.loads(message)

			rest_extended_data = await extend_websocket_data(message_json)

			topic = mqtt_topic_function(message_json, rest_extended_data)
			message = mqtt_message_function(message_json, rest_extended_data)

			print(f">>mqtt>> topic: {topic}: {message}")

			await mqttc.publish(topic,
					json.dumps(message).encode("UTF-8"))


asyncio.get_event_loop().run_until_complete(receive_deconz_messages())
