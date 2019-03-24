
global topic_generators
topic_generators = {}

global message_generators
message_generators = {}

def topic_generator(type):
	def decorator(fn):
		topic_generators[type] = fn
		return fn
	return decorator

def message_generator(type):
	def decorator(fn):
		message_generators[type] = fn
		return fn
	return decorator