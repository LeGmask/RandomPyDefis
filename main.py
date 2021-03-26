import os
import random
import discord
import humanize
from discord.ext import commands

from src.config import config
from src.database import Database
from src.callicode import Callicode 

bot = commands.Bot(command_prefix="~")
callicode = Callicode(config)
database = Database(config)
humanize.i18n.activate("fr_FR")

@bot.event
async def on_ready():
	print(f"Bot {bot.user.name} connected on {len(bot.guilds)} server{'s'*(len(bot.guilds)>1)}")


@bot.event
async def on_message(message):
	author = str(message.author.name).split(' ')[0]
	if author in config.USERS:

		if message.content[:8] == "~pydefis": # if command as the good prefix
			command = message.content[8:] # remove prefix `~pydefis`
			if "new" in command:
				challenges = callicode.getChallenges()
				args = command[command.find("new")+4:].split(' ')
				if not database.getChallenge() or "--ignore" in args:
					if not "--all" in args:
						if "--level" in args:
							try:
								level = int(args[args.index("--level")+1])
							except:
								await message.reply(content="Invalid usage of --level parameter", mention_author=False)
								return
							print(level)
							challenges = callicode.filter(challenges, level=level)
						if "--name" in args:
							try:
								name = command[command.index("--name \"")+8:]
								name = name[:name.index("\"")].lower()
								
							except:
								await message.reply(content="Invalid usage of --name parameter", mention_author=False)
								return
							
							challenges = callicode.filter(challenges, name=name) 
						challenges = database.removeDone(challenges) 
					if challenges:
						challenge = challenges[random.randint(0, len(challenges)-1)]
						if not "--ignore" in args:
							database.newChallenge(challenge)
						await message.reply(content=f"**Défi** : {challenge['name']}\n**Niveau** : {challenge['level']}\n**URL** : {challenge['url']}", mention_author=False)
						return
					else:
						await message.reply(content="_Pas de défis trouvé_", mention_author=False)
						return
				else:
					await message.reply(content="_Un defis est déjà en cours..._", mention_author=False)
			if "history" in command:
				challenge = database.getArchive()
				content=f"**Défi** : {challenge['name']}\n**Niveau** : {challenge['level']}\n**URL** : {challenge['url']}\n"
				for user in challenge["ranking"]:
					if challenge["ranking"][user]["state"] != "resolved":
						content += f"- **{user}**: {challenge['ranking'][user]['state']}"
					else:
						content += f"- **{user}**: résolu en {humanize.naturaldelta(database.getTimedelta(challenge,user))}\n"
				await message.reply(content=content, mention_author=False)

				return
			if database.getChallenge():
				if "coding" in command:
					if database.getState(author) != "coding":
						if database.getState(author) != "resolved":
							database.setCoding(author)
							await message.reply(content="_3, 2, 1, **GO**..._", mention_author=False)
						else:
							await message.reply(content="_Vous avez déjà résolu le défis..._", mention_author=False)
					else:
						await message.reply(content="_Vous codez déjà..._", mention_author=False)
				if "pause" in command:
					if database.getState(author) == "coding":
						database.setPause(author)
						await message.reply(content="_Eh ! calme ! c'est la pause..._", mention_author=False)
						
					else:
						await message.reply(content="_Vous devez commencer a coder avant de pouvoir mettre en pause..._", mention_author=False)
				if "resolved" in command:
					if database.getState(author) == "coding" :
						database.setResolved(author)
						await message.reply(content="_Bravo, :clap: ..._", mention_author=False)
						if database.checkResolved():
							database.archive()
							await message.reply(content="_Défi terminé :+1:, vous pouvez un choisir un nouveau `~pydefis new`..._", mention_author=False)

					else:
						await message.reply(content="_Vous devez coder avant de résoudre un défi..._", mention_author=False)
				if "stats" in command:
					challenge = database.getChallenge()
					content=f"**Défi** : {challenge['name']}\n**Niveau** : {challenge['level']}\n**URL** : {challenge['url']}\n"
					for user in challenge["ranking"]:
						if challenge["ranking"][user]["state"] != "resolved":
							content += f"- **{user}**: {challenge['ranking'][user]['state']} \n"
						else:
							content += f"- **{user}**: résolu en {humanize.naturaldelta(database.getTimedelta(challenge,user))}\n"
					await message.reply(content=content, mention_author=False)
				if "check" in command:
					if database.checkResolved():
						database.archive()
						await message.reply(content="_Défi terminé :+1:, vous pouvez un choisir un nouveau `~pydefis new`..._", mention_author=False)
					else :
						await message.reply(content="_Tout le monde n'a pas fini le défi..._", mention_author=False)

			else:
				await message.reply(content="_Aucun défi pour le moment..._", mention_author=False)

			



			


try:
	bot.run(config.DISCORD.token)
finally:
	print('EXITING GRACEFULLY')
