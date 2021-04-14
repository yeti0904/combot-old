import discord
import os
import json
import random
import sys
import datetime
import socket
from random import randrange
with open("banned.txt") as f:
	banned = f.read().splitlines()

client = discord.Client()

@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))
	activity = discord.Game(name="com help")
	await client.change_presence(activity=activity)

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	msgargs = str(message.content).split(" ")
	print(msgargs)
	count = 0
	for arg in msgargs:
		msgargs[count] = str(msgargs[count]).lower()
		count += 1
	if msgargs[0] == "com":
		if msgargs[1] == "id":
			if len(msgargs) == 2:
				await message.channel.send("```\nYour ID: " +str(message.author.id) +"\n```")
			if len(msgargs) == 3:
				name = msgargs[2]
				await message.channel.send("```\nThat user's ID: " +name[3:-1] +"\n```")
		if msgargs[1] == "economy":
			if len(msgargs) != 2:
				if msgargs[2] == "register":
					attempt = True
					try:
						f = open("economy/accounts/" +str(message.author.id) +".json", "x")
						f.close()
						f = open("economy/accounts/" +str(message.author.id) +".json", "w")
						f.write('[{ "bal":0, "job":"useless", "level":0 }]')
						f.close()
					except Exception as err:
						attempt = False
						await message.channel.send("```\nThere was an error creating your account.\n" +str(err) +"\n```")
					if attempt == True:
						await message.channel.send("```\nEconomy Account successfully created!\n```")
			else:
				await message.channel.send("```\nEconomy Help\ncom economy register - Register on the economy\n```")
		if msgargs[1] == "bal" and len(msgargs) == 2:
			if os.path.exists("economy/accounts/" +str(message.author.id) +".json"):
				#with open("economy/accounts/" +str(message.author.id) +".txt") as f:
				#	userinfo = f.read().splitlines()
				userinfo = open("economy/accounts/" +str(message.author.id) +".json", "r")
				userinfod = userinfo.read()
				userinfo.close()
				data = json.loads(userinfod)
				bal = data[0]["bal"]
				await message.channel.send("```\nYour balance:\nWallet: " +str(bal) +"\n```")
			else:
				await message.channel.send("```\nError! You don't have an account, create one with 'com economy register'!\n```")
		'''
		if msgargs[1] == "work":
			if os.path.exists("economy/accounts/" +str(message.author.id) +".txt"):
				userinfo = open("economy/accounts/" +str(message.author.id) +".txt", "r")
				userinfod = userinfo.read()
				userinfo.close()
				data = json.loads(userinfod)
				bal = data[0]["bal"]
				earn = random.randrange(20,70)
				jobs = ["chef","taxi driver","programmer","builder","architect","YouTuber","vet","doctor","fisherman"]
				myjob = jobs[randrange(0,int(len(jobs) - 1))]
				await message.channel.send("```\nYou worked as a " +myjob +" and earned " +str(earn) +"!\n```")
				data[0]["bal"] = bal + earn
				print(data)
				datac = json.dumps(data)
				userinfo = open("economy/accounts/" +str(message.author.id) +".txt", "w")
				userinfo.write(datac)
				userinfo.close()
			else:
				await message.channel.send("```\nError! You don't have an account, create one with 'com ecomomy register'!\n```")
		'''
		if len(msgargs) == 3 and msgargs[1] == "bal":
			name = msgargs[2]
			name = name[3:-1]
			print(name)
			if os.path.exists("economy/accounts/" +str(name) +".json"):
				userinfo = open("economy/accounts/" +str(name) +".json", "r")
				userinfod = userinfo.read()
				userinfo.close()
				data = json.loads(userinfod)
				bal = data[0]["bal"]
				await message.channel.send("```\nTheir balance:\nWallet: " +str(bal) +"\n```")
			else:
				await message.channel.send("```\nError! You don't have an account, create one with 'com ecomomy register'!\n```")
		if msgargs[1] == "admin-control":
			with open("admins.txt") as f:
				admins = f.read().splitlines()
			if str(message.author.id) in admins:
				if len(msgargs) != 2:
					if msgargs[2] == "shutdown":
						await message.channel.send("```\nShutting down.. Thank you for using ComBot!\n```")
						exit()
					if msgargs[2] == "refresh-banned":
						await message.channel.send("```\nRefreshing banned users\n```")
						with open("banned.txt") as f:
							banned = f.read().splitlines()
						await message.channel.send("```\nDone!\n```")
					'''
					if msgargs[2] == "ban":
						name = msgargs[3]
						name = name[3:-1]
						await message.channel.send("```\nBanning user..\n```")
						f = open("banned.txt", "a")
						f.write(str(name))
						f.close()
						await message.channel.send("```\nBanned!```\n")
					'''
					if msgargs[2] == "restart":
						await message.channel.send("```\nRestarting..\n```")
						os.execl(sys.executable, sys.executable, *sys.argv)
						await message.channel.send("```\nRestarted!\n```")
					if msgargs[2] == "reset-economy":
						await message.channel.send("```\nPreparing to reset Economy..\n```")
						os.system("touch economies && ls economy/accounts/ > economies")
						with open("economies") as f:
							economies = f.read().splitlines()
						await message.channel.send("```\nPrepared. Resetting Economy now.\n```")
						print(economies)
						for account in economies:
							print(account)
							userinfo = open("economy/accounts/" +str(account) +".txt", "w")
							towrite = json.dumps('[{"bal":0}]')
							userinfo.write(towrite)
							userinfo.close()
						await message.channel.send("```\nEconomy has been reset.\n```")
					if msgargs[2] == "status":
						if msgargs[3] == "play":
							activity = discord.Game(name=msgargs[4]).replace("-"," ")
							await client.change_presence(activity=activity)
						if msgargs[3] == "stream":
							await client.change_presence(activity=discord.Streaming(name=msgargs[4].replace("-"," "), url=msgargs[5]))
				else:
					await message.channel.send("```\nComBot Admin Panel\nshutdown - shutdown ComBot\nrestart - restart ComBot\nreset-economy - Reset ComBot economy\n```")
			else:
				await message.channel.send("```\nYou are not authorized to make this action.\n```")
		if msgargs[1] == "job":
			if len(msgargs) != 2:
				if msgargs[2] == "list":
					await message.channel.send("```\nComBot Jobs\nbin man - 500 ComCoins an hour (Level 0+)\nTesco cleaner - 2000 ComCoins an hour (Level 5+)\n```")
				if msgargs[2] == "get":
					jobs = ["binman","tescocleaner"]
					if os.path.exists("economy/accounts/" +str(message.author.id) +".json"):
						userinfo = open("economy/accounts/" +str(message.author.id) +".json", "r")
						userinfod = userinfo.read()
						userinfo.close()
						data = json.loads(userinfod)
						level = data[0]["level"]
						if msgargs[3] == "binman":
							await message.channel.send("```\nGetting job bin man..\n```")
							data[0]["job"] = "binman"
							datac = json.dumps(data)
							userinfo = open("economy/accounts/" +str(message.author.id) +".txt", "w")
							userinfo.write(datac)
							userinfo.close()
							await message.channel.send("```\nDone\n```")
						elif msgargs[3] == "tescocleaner":
							if level >= 4:
								await message.channel.send("```\nGetting job tesco cleaner...\n```")
								data[0]["job"] = "tescocleaner"
								await message.channel.send("```\nDone\n```")
								datac = json.dumps(data)
								userinfo = open("economy/accounts/" +str(message.author.id) +".txt", "w")
								userinfo.write(datac)
								userinfo.close()
								await message.channel.send("```\nDone\n```")
							else:
								await message.channel.send("```\nYou don't have enough levels to get this job! Min is 5\n```")
					else:
						await message.channel.send("```\nYou dont't have an Economy account! Create one with 'com economy register'!\n```")			
			else:
				await message.channel.send("```\nComBot Jobs help\nlist - list all jobs with pay and min level\n```")
		if msgargs[1] == "profile":
			userinfo = open("economy/accounts/" +str(message.author.id) +".json", "r")
			userinfod = userinfo.read()
			userinfo.close()
			data = json.loads(userinfod)
			await message.channel.send("```\nComBot Profile:\nUser ID: " +str(message.author.id) +"\n\nMoney:\nWallet: " +str(data[0]["bal"]) +"\n\nOther:\nLevel: " +str(data[0]["level"]) +"\n```")
		if msgargs[1] == "beg":
			responses = ["00I have no money!","49Take this you poor beggar","00Go away!","01Just take this and go away"]
			response = responses[randrange(0,int(len(responses) - 1))]
			say = response[2:]
			recieve = int(response[:2])
			jsoni = open("economy/accounts/" +str(message.author.id) +".json", "r")
			jsond = json.load(jsoni)
			jsoni.close()
			bal = jsond[0]["bal"]
			jsond[0]["bal"] = bal + recieve
			datac = json.dumps(jsond)
			userinfo = open("economy/accounts/" +str(message.author.id) +".json", "w")
			userinfo.write(datac)
			userinfo.close()
			await message.channel.send('```\n"' +str(say) +'"\nYou recieve: ' +str(recieve) +'\n```')
		if msgargs[1] == "help":
			with open("help.txt") as f:
				help = f.read()
			await message.channel.send("```\n" +help +"\n```")
		'''
		if msgargs[1] == "irc":
			if msgargs[2] == "link":
				ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				server = msgargs[3]
				Serverchannel = msgargs[4]
				botnick = "ComBot" +str(randrange(11111,99999))
				# Your bots nickname
				adminname = "ComBot" +str(randrange(11111,99999))
				#Your IRC nickname. On IRC (and most other places) I go by OrderChaos so that’s what I am using for this example.
				exitcode = "bye " + botnick
				ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
				ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "n", "UTF-8"))
				#We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
				ircsock.send(bytes("NICK "+ botnick +"n", "UTF-8")) 
				# assign the nick to the bot
				def joinchan(chan): # join channel(s)
					ircsock.send(bytes("JOIN "+ chan +"n", "UTF-8"))
				ircmsg = ""
				while ircmsg.find("End of /NAMES list.") == -1:
					ircmsg = ircsock.recv(2048).decode("UTF-8")
					ircmsg = ircmsg.strip('nr')
					await message.channel.send("```\n" +ircmsg +"\n```")
					def ping():
						ircsock.send(bytes("PONG :pingisn", "UTF-8"))
				def main():
					joinchan(channel)  
				while 1:
					ircmsg = ircsock.recv(2048).decode("UTF-8")
					ircmsg = ircmsg.strip('nr')
					await message.channel.send("```\n" +ircmsg +"\n```")
		'''
client.run("put bot token here")
