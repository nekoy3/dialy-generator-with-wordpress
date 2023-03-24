import json
import discord
from discord import app_commands

#キーワード引数
#javadrive.jp/python/userfunc/index6.html
class BotClient(discord.Client):
    def __init__(self, guild_id, channel_id, wp_client):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self) #全てのコマンドを管理するCommandTree型オブジェクトを生成
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.wp_client = wp_client

    async def setup_hook(self):
        guild=discord.Object(id=self.guild_id)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
    
    def make_embed(self, title, description, color=0x000000):
        embed = discord.Embed(title=title,description=description,color=color)
        return embed
    
    async def send_message(self, msg):
        l = len(msg)
        msg_list = []
        c = self.get_channel(self.channel_id)
        while l >= 2000:
            msg_list.append(msg[:1998])
            msg = msg[1999:]
            l = len(msg)
        msg_list.append(msg)

        for m in msg_list:
            await c.send(m)
    
    async def send_embed(self, embed):
        c = self.get_channel(self.channel_id)
        await c.send(embed=embed)

    async def on_ready(self):
        print("Bot ready.")
        """
        p = self.wp_client.test_post()
        e = self.make_embed("投稿テスト", f"投稿が完了しました。\nid: {p['id']}\ntitle: {p['title']['rendered']}\nlink: {p['link']}")
        await self.send_embed(e)
        """