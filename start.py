import discord
import discordBot

class MyBot:
    def __init__(self, cfg, wp_client):
        self.intents = discord.Intents.all() #全ての権限を許可
        #botを動かすためのインスタンスを生成
        self.client = discordBot.BotClient(cfg.guild_id, cfg.channel_id, wp_client, intents=self.intents)
        print('Starting...')