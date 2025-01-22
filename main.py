import discord
import flask
import os
import colorama
import requests
import threading
import asyncio
import logging
import time

from discord.ext import commands
from colorama import Fore
from flask import Flask, jsonify, request
from time import sleep

app = Flask(__name__)
token = os.getenv("TOKEN")
url = os.getenv("URL")
logs = os.getenv("LOGS_URL")
owner = 1224392642448724012

whitelisted_users = {
    "1224392642448724012": 1224392642448724012
}

banned_users = {}

usage_banned_users = {}

auth_headers = {
    "Authorization": token
}

@app.route("/")
def index():
    return "https://discord.gg/jQ3vCYCJZD"

@app.route("/ban", methods=["POST"])
def ban():
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
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500
    
@app.route("/unban", methods=["POST"])
def unban():
    data = request.get_json()
    user = data.get("user")
    sender = str(data.get("sender"))
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
    
    if not whitelisted_users[sender]:
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
    sender = str(data.get("sender"))
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
    
    if not whitelisted_users[sender]:
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
    
    if not whitelisted_users[sender]:
        return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
    
    try:
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
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/bans", methods=["GET"])
def bans():
    try:
        requests.post(logs, json={
            "content": None,
            "embeds": [
                {
                    "title": "Hyperskidded Hub",
                    "description": f"Bans have been fetched.",
                    "color": 7340207,
                    "footer": {
                        "text": "Hyperskidded Hub",
                        "icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
                    }
                }
            ],
        })
        return jsonify(banned_users), 200
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/usage-bans", methods=["GET"])
def usagebans():
    try:
        requests.post(logs, json={
            "content": None,
            "embeds": [
                {
                    "title": "Hyperskidded Hub",
                    "description": f"Usage bans have been fetched.",
                    "color": 7340207,
                    "footer": {
                        "text": "Hyperskidded Hub",
                        "icon_url": "https://cdn.discordapp.com/icons/1320734306053918782/9cf4f4109ed0594691e765fef657a957.webp?size=512"
                    }
                }
            ],
        })
        return jsonify(usage_banned_users), 200
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/whitelist", methods=["POST"])
def whitelist():
    data = request.get_json()
    user = data.get("user_id")
    sender = str(data.get("sender"))
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
    
    if sender != str(owner):
        return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
    
    try:
        if whitelisted_users[user]:
            return jsonify({"status": "already whitelisted"}), 400
        else:
            whitelisted_users[user] = user
            return jsonify({"status": "success"}), 200
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500
    
@app.route("/remove-whitelist", methods=["POST"])
def removewhitelist():
    data = request.get_json()
    user = data.get("user_id")
    sender = str(data.get("sender"))
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
    
    if sender != str(owner):
        return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
    
    try:
        if whitelisted_users[user]:
            del whitelisted_users[user]
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
        sentrequest = requests.post(url+"ban", json={"user": user, "authorization": token, "sender": str(ctx.author.id), "reason": reason})
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
        sentrequest = requests.post(url+"unban", json={"user": user, "authorization": token, "sender": str(ctx.author.id)})
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
        sentrequest = requests.post(url+"usage-unban", json={"user": user, "authorization": token, "sender": str(ctx.author.id)})
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
        sentrequest = requests.post(url+"whitelist", json={"user": str(user.id), "authorization": token, "sender": str(ctx.author.id)})
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
async def removewhitelist(ctx, user: discord.User):
    try:
        sentrequest = requests.post(url+"remove-whitelist", json={"user": str(user.id), "authorization": token, "sender": str(ctx.author.id)})
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
