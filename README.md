# IP-Bot
## Description
Discord bot that fetches the public IP of the computer hosting it and provides commands to get information about the Minecraft server under that IP address.

### Author
Quix#5870

### Available commands
Prefix: `./`

- `ip` returns the public IP of the computer hosting the server
  ![ip](https://i.imgur.com/u2aKzCn.png)
- `status` returns information about the Minecraft server (i.e. latency, online players)
  ![status](https://i.imgur.com/tWvXoMw.png)
- `help` returns a menu with all available commands and information about the bot

## How to deploy
Firstly, you have to install the following libraries: discord.py, requests, bs4, mcstatus

To install them all at once, you can use:
```commandline
pip install discord.py requests bs4 mcstatus
```

If you have Python 2.7 installed, you will need to use pip3 instead of pip.

Next, you need to create a file named `config.json` that contains your discord bot token, preferred prefix, and server port.
```json
{
  "Token": "<your_token>",
  "Prefix": "./",
  "Port": 25565
}
```

Finally, to start the bot, run `bot.py`.

## Minimum requirements
- Python version: 3.8

## APIs and libraries used
- Server's public IP (API): [ipify.org](https://www.ipify.org/)
- Minecraft server statistics (Library): [mcstatus](https://github.com/Dinnerbone/mcstatus)