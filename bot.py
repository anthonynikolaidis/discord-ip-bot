import json
from datetime import datetime

import requests

from mcstatus import MinecraftServer

import logging
import discord
from discord.ext import commands
from discord.utils import find

logging.basicConfig(level=logging.INFO)

with open('config.json') as data:
    config = json.load(data)

bot = commands.Bot(command_prefix=config["Prefix"])
bot.remove_command("help")

embed_color = discord.Color.green()
icon_url = "https://i.imgur.com/4sg6CWv.png"


def get_ip():
    url = "https://api.ipify.org"
    public_ip = requests.get(url).text

    return public_ip


def get_ip_info():
    public_ip = get_ip()

    what_is_my_ip_url = f"https://www.whatismyip.com/{public_ip}/"

    global server
    server = MinecraftServer(public_ip, server_port)

    return {
        "IP": public_ip,
        "Link": what_is_my_ip_url
    }


initial_ip = get_ip()
server_port = config["Port"]

server = MinecraftServer(initial_ip, server_port)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f"Use {config['Prefix']}ip to get started!"))


@bot.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        embed = discord.Embed(
            description="• Use `./ip` to get the server IP!\n"
                        "• To see a list of available commands use `./help`.",
            timestamp=datetime.utcnow(),
            colour=embed_color
        )
        embed.set_author(name="Thanks for inviting me!", icon_url=icon_url)
        embed.set_footer(text="Created by Quix#5870")
        await general.send(embed=embed)


@bot.command()
async def ip(ctx):
    ip_info = get_ip_info()

    server_ip = ip_info["IP"]
    link = ip_info["Link"]

    embed = discord.Embed(
        timestamp=datetime.utcnow(),
        color=embed_color
    )
    embed.set_author(name="IP-Bot | Get server IP", url=link, icon_url=icon_url)

    embed.add_field(name="Server IP", value=server_ip, inline=False)

    msg = await ctx.send(embed=embed)


@bot.command()
async def status(ctx):
    wait_embed = discord.Embed(
        description="Querying server... Please, wait.",
        timestamp=datetime.utcnow(),
        color=embed_color
    )
    wait_embed.set_author(name="IP-Bot | Get server status", icon_url=icon_url)

    wait_msg = await ctx.send(embed=wait_embed)

    get_ip_info()

    query = server.query()
    server_status = server.status()

    player_string = ""
    for i in range(0, len(query.players.names)):
        player_string += query.players.names[i].split("(")[0] + "\n"

    if player_string == "":
        player_string = "No players are online"

    embed = discord.Embed(
        title=query.motd,
        description="The server replied in {0} ms.".format(round(server_status.latency)),
        timestamp=datetime.utcnow(),
        color=embed_color
    )
    embed.set_author(name="IP-Bot | Get server status", icon_url=icon_url)

    embed.add_field(
        name="Online players (" + str(server_status.players.online) + "/" + str(server_status.players.max) + ")",
        value=player_string, inline=False)

    # await wait_msg.edit(embed=embed)     # edit sent embed

    msg = await ctx.send(embed=embed)
    await bot.http.delete_message(ctx.channel.id, wait_msg.id)  # deletes wait message


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        timestamp=datetime.utcnow(),
        color=embed_color
    )
    embed.set_author(name="IP-Bot | Help", icon_url=icon_url)

    embed.add_field(name="Command prefix", value="`./`", inline=False)
    embed.add_field(name="List of commands",
                    value="• `ip` returns the public IP of the computer hosting the server\n"
                          "• `status` returns information about the Minecraft server (i.e. latency, online players)\n"
                          "• `help` returns this menu",
                    inline=False)
    embed.add_field(name="Github repository",
                    value="[www.github.com/anthonynikolaidis/discord-ip-bot]"
                          "(https://github.com/anthonynikolaidis/discord-ip-bot)",
                    inline=False)

    embed.set_footer(text="Created by Quix#5870")

    msg = await ctx.send(embed=embed)


bot.run(config["Token"])
