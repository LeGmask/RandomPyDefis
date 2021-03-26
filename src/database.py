import os
import json
from datetime import datetime, timedelta


class Database:
	def __init__(self, config) -> None:
		self.config = config
		try:
			self.loadDatabase()
		except:
			self.migrate()
			self.loadDatabase()
	
	def loadDatabase(self):
		self.Users = self.loadFile("Users")
		self.History = self.loadFile("History")
		self.Challenge = self.loadFile("Challenge")
	
	def newChallenge(self, challenge):
		self.Challenge = {
			"name": challenge["name"],
			"level": challenge["level"],
			"url": challenge["url"],
			"ranking": { 
				user["name"]: {
					"state": "idle",
					"current": None,
					"time": []
				} for user in self.Users 
			},
		}
		self.writeFile("Challenge", self.Challenge)

	def getChallenge(self):
		return self.Challenge

	def getState(self, User):
		return self.Challenge["ranking"][User]["state"]

	def setCoding(self, User):
		self.Challenge["ranking"][User]["state"] = "coding"
		self.Challenge["ranking"][User]["current"] = datetime.timestamp(datetime.now())
		self.writeFile("Challenge", self.Challenge)

	def setPause(self, User):
		self.Challenge["ranking"][User]["state"] = "pause"
		self.Challenge["ranking"][User]["time"].append((self.Challenge["ranking"][User]["current"],datetime.timestamp(datetime.now())))
		self.Challenge["ranking"][User]["current"] = None
		self.writeFile("Challenge", self.Challenge)

	def setResolved(self, User):
		self.Challenge["ranking"][User]["state"] = "resolved"
		self.Challenge["ranking"][User]["time"].append((self.Challenge["ranking"][User]["current"],datetime.timestamp(datetime.now())))
		self.Challenge["ranking"][User]["current"] = None
		self.writeFile("Challenge", self.Challenge)

	def getTimedelta(self, Challenge, User):
		delta = []
		for i in Challenge["ranking"][User]["time"]:
			delta.append(datetime.fromtimestamp(i[1])-datetime.fromtimestamp(i[0]))
		return sum(delta, timedelta())
	
	def checkResolved(self):
		for user in self.Challenge["ranking"]:
			if self.Challenge["ranking"][user]["state"] != "resolved":
				return False
		return True

	def newUser(self, user):
		self.Users.append({
			"id": len(self.Users),
			"name": user["name"]
		})
		self.writeFile("Users", self.Users)
	
	def removeDone(self, challenges):
		done = []
		filtered = []
		for i in self.History:
			done.append(i["name"])
		for i in challenges:
			if i["name"] not in done:
				filtered.append(i)
		return filtered


	def archive(self):
		self.History.append(self.Challenge)
		self.writeFile("History", self.History)
		self.Challenge.clear()
		self.writeFile("Challenge", self.Challenge)
	
	def getArchive(self):
		return self.History[len(self.History)-1]
	
	def getArchives(self):
		return self.History

	def loadFile(self, file):
		with open(os.path.join(os.path.dirname(__file__), f'../database/{file}.json'), "r") as file:
				return json.load(file)

	def writeFile(self, file, content):
		with open(os.path.join(os.path.dirname(__file__), f'../database/{file}.json'), "w") as file:
			file.write(json.dumps(content))

	def migrate(self):
		# Users migration
		self.Users = []
		for user in self.config.USERS:
			self.newUser({"name": user}) 
		self.writeFile("Users", self.Users)
		# Challenge migration
		self.writeFile("Challenge", None)
		# History migration
		self.writeFile("History", [])
