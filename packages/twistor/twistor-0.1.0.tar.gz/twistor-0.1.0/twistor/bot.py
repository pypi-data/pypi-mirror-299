import discord
from discord.ext import commands
import os

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable the messages intent
intents.message_content = True  # Enable message content intent

# Define the bot with intents
def create_bot(prefix):
    bot = commands.Bot(command_prefix=prefix, intents=intents)

    # Simple Twistor interpreter
    def interpret_twt(file_name):
        # Check if the .twt file exists
        if not os.path.isfile(file_name):
            return None  # Return None if the file doesn't exist
        
        with open(file_name, 'r') as file:
            lines = file.readlines()
        
        # Parse each line in the .twt file
        for line in lines:
            line = line.strip()
            if line.startswith("mesg ="):
                # Extract the message content
                message = line.split('=')[1].strip().strip('()').strip('"')
                return message  # Return the message

    # Automatically discover and register commands based on .twt files
    for file_name in os.listdir("."):  # Assuming the .twt files are in the current directory
        if file_name.endswith(".twt"):
            # Extract the command name from the filename (e.g., 'hello-world.twt' -> 'hello-world')
            command_name = os.path.splitext(file_name)[0]

            # Define the command dynamically
            async def dynamic_command(ctx, command_name=command_name):
                # Load and interpret the Twistor file for the command
                message = interpret_twt(f"{command_name}.twt")
                
                if message:
                    await ctx.send(message)
                else:
                    await ctx.send(f"No message found in {command_name}.twt")
            
            # Register the dynamic command with the bot
            bot.command(name=command_name)(dynamic_command)

    # Error handler for command not found
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Sorry, that command does not exist. Please try again!")

    return bot