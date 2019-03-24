from server_lib import topic_generator, message_generator

@topic_generator('ZHAPressure')
def zhapress_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'pressure', rest_message['name']]))

@message_generator('ZHAPressure')
def zhapress_message(websocket_message, rest_message):
	return {
		'event': websocket_message['e'],
		'pressure': websocket_message['state']['pressure'],
		'battery': websocket_message['config']['battery'],
		}



@topic_generator('ZHATemperature')
def zhatemp_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'temperature', rest_message['name']]))

@message_generator('ZHATemperature')
def zhatemp_message(websocket_message, rest_message):
	return {
		'event': websocket_message['e'],
		'temperature': websocket_message['state']['temperature'],
		}



@topic_generator('ZHAHumidity')
def zhahumidity_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'humidity', rest_message['name']]))

@message_generator('ZHAHumidity')
def zhahumidity_message(websocket_message, rest_message):
	return {
		'event': websocket_message['e'],
		'temperature': websocket_message['state']['humidity'],
		'battery': websocket_message['config']['battery'],
		}




@topic_generator('ZHAOpenClose')
def zhaopenclose_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'openClose', rest_message['name']]))

@message_generator('ZHAOpenClose')
def zhaopenclose_message(websocket_message, rest_message):
	return {
		'event': websocket_message['e'],
		'state': 'open' if websocket_message['state']['open'] else 'closed',
		}




@topic_generator('ZHASwitch')
def zhaswitch_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'switch', rest_message['name']]))

@message_generator('ZHASwitch')
def zhaswitch_message(websocket_message, rest_message):
	button_map = {
		1002: 'left',
		2002: 'right',
		3002: 'both'
	}
	return {
		'event': websocket_message['e'],
		'button': button_map[websocket_message['state']['buttonevent']],
		}
