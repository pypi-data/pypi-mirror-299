import discord
import requests

class Guild(discord.Guild):

    @property
    def boost_count(self):
        return self.premium_subscription_count
