# Twistor
A language or a package used to make discord bots..... :)

## Usage

```python
from twistor.bot import create_bot

bot = create_bot(prefix="!")
bot.run("YOUR_DISCORD_BOT_TOKEN")
```
## Features

- Automatically registers Discord bot commands based on `.twt` files.
- Each `.twt` file contains a message and an optional description for the command.
- Supports custom message responses for commands without hardcoding.

## Installation

You can install `twistor` via pip:

```bash
pip install twistor
```
Creating Commands with .twt Files
In the same directory where your bot is running, create .twt files for each command.

For example, to create a hello-world command, create a hello-world.twt file:


```
mesg = "Hello, world!"
```
When the user types !hello-world in the Discord server, the bot will respond with Hello, world!.

# Creating a main.py

```python
from twistor.bot import create_bot

# Define your bot prefix
bot = create_bot(prefix="!")

# Run your bot
bot.run("YOUR_DISCORD_BOT_TOKEN")
```
# License
This project is licensed under the MIT License.

```sql 
This provides full instructions, usage examples, and explanation of how to set up commands using `.twt` files. Let me know if any changes are needed!
```