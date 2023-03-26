import discord
from discord import app_commands
import asyncio

class DiscordController(discord.Client):
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


#時間がかかる処理を行うメソッドをすべてこのクラスに格納する
class AsynchronousMethods:
    async def write_diary(self):
        await self.sub_obj.send_message("Please enter a title.")
        while True:
            await asyncio.sleep(0.2)
            break


#キーワード引数
#javadrive.jp/python/userfunc/index6.html
class BotClient(DiscordController):
    def __init__(self, guild_id, channel_id, wp_client):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self) #全てのコマンドを管理するCommandTree型オブジェクトを生成
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.wp_client = wp_client
        self.async_methods = AsynchronousMethods()

        #sub_objについて
        #sub_objはこのクラス自身を保持しており、AsynchronousMethosクラスのインスタンスが保持している。
        #このインスタンスであるasync_methodsがこのBotClientクラスが持つメソッド(継承含む、send_messageメソッドなど)
        #にアクセスできるようにするためにはasync_methodsｵﾌﾞｼﾞｪｸﾄ自身がこのサブクラス自体を保持する必要がある
        #これ絶対正攻法じゃないよね
        self.async_methods.sub_obj = self

        #デコレータを直接付与すると、コンストラクタ実行前に実行されnot definedになるためあと付けデコレータする
        self.make_diary = self.tree.command(name="write_diary", description="日記の記述を開始します。")(self.make_diary)

    async def setup_hook(self):
        guild=discord.Object(id=self.guild_id)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
    
    def make_embed(self, title, description, color=0x000000):
        embed = discord.Embed(title=title,description=description,color=color)
        return embed

    async def on_ready(self):
        print("Bot ready.")
        """
        p = self.wp_client.test_post()
        e = self.make_embed("投稿テスト", f"投稿が完了しました。\nid: {p['id']}\ntitle: {p['title']['rendered']}\nlink: {p['link']}")
        await self.send_embed(e)
        """
    
    async def make_diary(self, interaction):
        asyncio.create_task(self.async_methods.write_diary())
        await interaction.response.send_message("done")