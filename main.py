import discord
import os
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

client = commands.Bot(intents=discord.Intents.all(), command_prefix=".")

@client.event
async def on_ready(): 
  # Setting `Playing ` status
  await client.change_presence(activity=discord.Game(name=".gethelp"))
  print('We have logged in as {0.user}'.format(client))

# CTAhelp
@client.command()
async def redlinehelp(ctx):
  async with ctx.message.channel.typing():
    help0 = "Need help for the .redline command? i gotchu homie :)\n\n"
    help = "**Capitalization is not needed, and you MUST exclude spaces & slashes.\n**"
    help01 = "Example: \n95th/Dan Ryan -> 95thDanRyan\nClark/Division -> Clarkdivision\n"
    help1 = "\nExample of correct usage for \".redline\":\n"
    help2 = ".redline 95thdanryan\n\n"
    help3 = "Here's an image showing all the red line stops.\n"
    help4 = "STAY SAFE OUT THERE!!"
    helpmsg = help0 + help + help01 + help1 + help2 + help3 + help4
    await ctx.channel.send(helpmsg)
    await ctx.channel.send(file=discord.File('RedLine.jpg'))

# CTA Tracker API
cta_stop_ids = {
    "95thdanryan"	:	"40450",
    "87th"	:	"41430",
    "79th"	:	"40240",
    "69th"	:	"40990",
    "63rd"	:	"40910",
    "garfield"	:	"41170",
    "47th"	:	"41230",
    "sox35th"	:	"40190",
    "cermakchinatown"	:	"41000",
    "roosevelt"	:	"41400",
    "harrison"	:	"41490",
    "jackson"	:	"40560",
    "monroe"	:	"41090",
    "lake"	:	"41660",
    "grand"	:	"40330",
    "chicago"	:	"41450",
    "clarkdivision"	:	"40630",
    "northclybourn"	:	"40650",
    "fullerton"	:	"41220",
    "belmont"	:	"41320",
    "addison"	:	"41420",
    "sheridan"	:	"40080",
    "wilson"	:	"40540",
    "lawrence"	:	"40770",
    "argyle"	:	"41200",
    "berwyn"	:	"40340",
    "brynmawr"	:	"41380",
    "thorndale"	:	"40880",
    "granville"	:	"40760",
    "loyola"	:	"41300",
    "morse"	:	"40100",
    "jarvis"	:	"41190",
    "howard"	:	"40900"
}

api_key = "1a222e67b4f940ce8a3e6031f9e98226"
base_url = "http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key="

@client.command()
async def redline(ctx, *, stop: str):
# async def redline(ctx):
    channel = ctx.message.channel
    stop_name = ""
    try: 
      stop_name = cta_stop_ids[stop.lower()]
      # print(stop_name)
      complete_url = base_url + api_key + "&mapid=" + stop_name + "&max=4&rt=Red"
      response = requests.get(complete_url)
      # Parse the HTML data with BeautifulSoup
      soup = bs(response.text, 'html.parser')
      # Extract and print the values of errcd, stanm, destnm, and arrt tags
      errcd = soup.find('errcd').text
      
      # Station names
      stanm_tags = soup.find_all('stanm')
      # Direction names
      destnm_tags = soup.find_all('destnm')
      # Arrival times
      arrt_tags = soup.find_all('arrt')
    
      if errcd == '0':
          async with channel.typing():
              # Station names
              stanm_tags = soup.find_all('stanm')
              # Direction names
              destnm_tags = soup.find_all('destnm')
              # Arrival times
              arrt_tags = soup.find_all('arrt')
  
              # Converting arrival times to 12 hour format
              new_arrt_tags = [""] * len(arrt_tags)
              for i in range(len(arrt_tags)):
                test = arrt_tags[i].text.split(' ')[1]
                formatted_time = datetime.strptime(test, "%H:%M:%S").strftime("%I:%M %p")
                new_arrt_tags[i] = formatted_time
  
              # Assembling discord bot reply
              embed = discord.Embed(
              title=f"Upcoming arrivals for {stanm_tags[0].text}",
              color=0x7289DA,
              timestamp=ctx.message.created_at,
              )
              for i in range(len(arrt_tags)):
                embed.add_field(name=f"{stanm_tags[i].text} ({destnm_tags[i].text})",
                          value=f"{new_arrt_tags[i]}",
                          inline=False)
              embed.set_footer(text="Data retrieved from CTA Train Tracker API")
  
              await channel.send(embed=embed)

      else:
          await channel.send("Stop not found, try again!")
    except KeyError:
      await channel.send("Stop mispelled or stop not found, please use \".redlinehelp\" for instructions.")
    except MissingRequiredArgument:
      await channel.send("Stop mispelled or stop not found, please use \".redlinehelp\" for instructions.")
    
# Clear chat
# @client.command()
# async def clear(ctx):
#   await ctx.channel.purge()

# Define a custom error handler using try-except
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Stop not found, please use \".redlinehelp\" for instructions.")
    else:
        # Handle other errors or let discord.py handle them
        pass
  
# Hello
@client.command()
async def hello(ctx):
  async with ctx.message.channel.typing():
    await ctx.channel.send('Hello!')

# GetHelp
@client.command()
async def gethelp(ctx):
  async with ctx.message.channel.typing():
    msg = "**Available commands:**\n"
    msg1 = ".hello\n.redline\n.redlinehelp"
    full = msg + msg1
    await ctx.channel.send(full)

my_secret = os.environ['TOKEN']
client.run(my_secret)

# Guide:
# https://stackoverflow.com/questions/63486570/how-to-make-a-weather-command-using-discord-py-v1-4-1

# Host for free:
# https://www.techwithtim.net/tutorials/discord-py/hosting-a-discord-bot-for-free

# Stocks
# https://www.alphavantage.co/

# API List
# https://github.com/public-apis/public-apis#index