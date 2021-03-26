import os
import json

with open(os.path.join(os.path.dirname(__file__), '../config.json'), "r", encoding='utf-8') as file:
	config_default = json.load(file)
with open(os.path.join(os.path.dirname(__file__), '../config_override.json'), "r", encoding='utf-8') as file:
	config_override = json.load(file)

def config_field(names):
	global config_default, config_override
	def load(cfg):
		ret = cfg
		for name in names:
			if not name in ret:
				return None
			ret = ret[name]
		return ret
	return load(config_override) or load(config_default)

class config:
	PREFIX = config_field(["PREFIX"])
	USERS = config_field(["USERS"])
	class CALLICODE:
		baseURL = config_field(["CALLICODE", "baseURL"])

	class DISCORD:
		token = config_field(["DISCORD", "TOKEN"])
