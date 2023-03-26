from configIO import ConfigClass
from connectWP import WpClass
from discordBot import BotClient

cfg = ConfigClass()
wp_client = WpClass(cfg.url, cfg.username, cfg.password)
bot_client = BotClient(cfg.guild_id, cfg.channel_id, wp_client)
print('Starting...')

bot_client.run(cfg.token)