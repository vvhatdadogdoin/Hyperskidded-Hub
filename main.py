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
owner = 1224392642448724012

whitelisted_users = [
    1224392642448724012
]

banned_users = []

usage_banned_users = []

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
    sender = data.get("sender")
    authorization = data.get("authorization")

    if authorization is not token:
        return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
    
    if not sender in whitelisted_users:
        return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
    
    try:
        banned_users.append(user)
        return jsonify({"status": "success"}), 200
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500
    
@app.route("/usage-ban", methods=["POST"])
def usage_ban():
    data = request.get_json()
    user = data.get("user")
    sender = data.get("sender")
    authorization = data.get("authorization")

    if authorization is not token:
        return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
    
    if not sender in whitelisted_users:
        return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
    
    try:
        usage_banned_users.append(user)
        return jsonify({"status": "success"}), 200
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/bans", methods=["GET"])
def bans():
    try:
        return jsonify({"bans": banned_users}), 200
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500

@app.route("/whitelist", methods=["POST"])
def whitelist():
    data = request.get_json()
    user = data.get("user_id")
    sender = data.get("sender")
    authorization = data.get("authorization")

    if authorization is not token:
        return jsonify({"status": "forbidden", "error": "You do not have a valid authorization key."}), 404
    
    if sender is not owner:
        return jsonify({"status": "forbidden", "error": "You're not authorized."}), 404
    
    try:
        whitelisted_users.append(user)
        return jsonify({"status": "success"}), 200
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
async def ban(ctx, user: str):
    try:
        sentrequest = requests.post(url+"ban", json={"user": user, "authorization": token, "sender": ctx.author.id})
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
                description = "Banned user: "+user
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
async def usageban(ctx, user: str):
    try:
        sentrequest = requests.post(url+"usage-ban", json={"user": user, "authorization": token, "sender": ctx.author.id})
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
                description = "Banned user "+user+" from using Hyperskidded Hub."
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
                description = "Whitelisted user "+user
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
    webserver = threading.Thread(target = main1, daemon=True)
    # bot = threading.Thread(target = main2, daemon=True)
    
    webserver.start()

    bot.run(token)
    
    webserver.join()
    # bot.join()
