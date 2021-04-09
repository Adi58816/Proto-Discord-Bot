# importing modules
import discord
import requests
import io
import json
from PIL import Image, ImageFont, ImageDraw
from discord.ext import commands
from datetime import datetime


class Ferma(commands.Cog):

    def __init__(self, client):
        self.client = client
        
# setup for cog
def setup(client):
    client.add_cog(Ferma(client))
