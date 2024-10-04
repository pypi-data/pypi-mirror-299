import discord


def get_boost_count(self):
    return self.premium_subscription_count


discord.Guild.boost_count = property(get_boost_count)
