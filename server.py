#!/usr/bin/env python

import asyncio
import aiohttp
import websockets
import json
import yaml
import aiomqtt

from server_lib import topic_generators, message_generators
import topics

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

def mqtt_topic_function(websocket_message, rest_extended_data):
	type = rest_extended_data['type']
	
	try:
		if type in topic_generators:
			fnct = topic_generators[type]
			return cfg['mqtt']['topic_root'] + fnct(websocket_message, rest_extended_data)
	except:
		pass
	
	return cfg['mqtt']['topic_root'] + '/'.join(filter(None, [websocket_message['r'], rest_extended_data['type'], rest_extended_data['name']]))

def mqtt_message_function(websocket_message, rest_extended_data):
	type = rest_extended_data['type']

	try:
		if type in message_generators:
			fnct = message_generators[type]
			return fnct(websocket_message, rest_extended_data)
	except:
		pass
	
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
			print(f"No extended REST data available for {websocket_json['r']}")
			pass
		
		return {}

@asyncio.coroutine
async def send_mqtt(topic, message):
	mqttc = aiomqtt.Client(asyncio.get_event_loop(), "deconz-to-mqtt")
	await mqttc.connect(cfg['mqtt']['host'], cfg['mqtt']['port'], cfg['mqtt']['timeout'])

	mqttc.publish(topic, json.dumps(message).encode("UTF-8"))

	mqttc.disconnect()

@asyncio.coroutine
async def websocket_message_loop(websocket):
	async for message in websocket:
		print(f"<<deconz<< {message}")
		message_json = json.loads(message)

		rest_extended_data = await extend_websocket_data(message_json)

		topic = mqtt_topic_function(message_json, rest_extended_data)
		message = mqtt_message_function(message_json, rest_extended_data)

		print(f">>mqtt>> topic: {topic}: {message}")
		await send_mqtt(topic, message)

@asyncio.coroutine
async def receive_deconz_messages():
	while True:
		try:
			async with websockets.connect(cfg['deconz']['websocket_url']) as websocket:
				await websocket_message_loop(websocket)
				
		except:
			pass



asyncio.get_event_loop().run_until_complete(receive_deconz_messages())
