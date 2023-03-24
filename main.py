from configIO import ConfigClass
from connectWP import WpClass
from discordBot import BotClient

class MyBot:
    def __init__(self, cfg, wp_client):
        self.client = BotClient(cfg.guild_id, cfg.channel_id, wp_client)
        print('Starting...')

cfg = ConfigClass()
wp_client = WpClass(cfg.url, cfg.username, cfg.password)
mybot = MyBot(cfg, wp_client)

mybot.client.run(cfg.token)