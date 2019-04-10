from server_lib import topic_generator, message_generator, failsafe

@topic_generator('ZHAPressure')
def zhapress_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'pressure', rest_message['name']]))

@message_generator('ZHAPressure')
def zhapress_message(websocket_message, rest_message):
	return {
		'event': websocket_message['e'],
		'pressure': failsafe(lambda : websocket_message['state']['pressure']),
		'battery': failsafe(lambda : websocket_message['config']['battery']),
		}



@topic_generator('ZHATemperature')
def zhatemp_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'temperature', rest_message['name']]))

@message_generator('ZHATemperature')
def zhatemp_message(websocket_message, rest_message):
	return {
		'event': websocket_message['e'],
		'temperature': failsafe(lambda : websocket_message['state']['temperature'] / 100),
		'battery': failsafe(lambda : websocket_message['config']['battery']),
		}



@topic_generator('ZHAHumidity')
def zhahumidity_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'humidity', rest_message['name']]))

@message_generator('ZHAHumidity')
def zhahumidity_message(websocket_message, rest_message):
	return {
		'event': websocket_message['e'],
		'humidity': failsafe(lambda : websocket_message['state']['humidity'] / 100),
		'battery': failsafe(lambda : websocket_message['config']['battery']),
		}




@topic_generator('ZHAOpenClose')
def zhaopenclose_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'openClose', rest_message['name']]))

@message_generator('ZHAOpenClose')
def zhaopenclose_message(websocket_message, rest_message):
	return {
		'event': websocket_message['e'],
		'state': failsafe(lambda : 'open' if websocket_message['state']['open'] else 'closed'),
		'battery': failsafe(lambda : websocket_message['config']['battery']),
		'temperature': failsafe(lambda : websocket_message['config']['temperature']),
		}




@topic_generator('ZHASwitch')
def zhaswitch_topic(websocket_message, rest_message):
	return '/'.join(filter(None, [websocket_message['r'], 'switch', rest_message['name']]))

@message_generator('ZHASwitch')
def zhaswitch_message(websocket_message, rest_message):
	button_map = {
		1002: 'button1',
		2002: 'button2',
		3002: 'button3',
		4002: 'button4',
		5002: 'button5',
	}
	return {
		'event': websocket_message['e'],
		'button': failsafe(lambda : button_map[websocket_message['state']['buttonevent']]),
		'battery': failsafe(lambda : websocket_message['config']['battery']),
		'temperature': failsafe(lambda : websocket_message['config']['temperature']),
		}
