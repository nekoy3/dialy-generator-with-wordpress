from start import MyBot
from configIO import ConfigClass
from connectWP import WpClass

cfg = ConfigClass()
wp_client = WpClass(cfg.url, cfg.username, cfg.password)
mybot = MyBot(cfg, wp_client)

mybot.client.run(cfg.token)