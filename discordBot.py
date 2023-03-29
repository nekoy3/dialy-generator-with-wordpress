import discord
from discord import app_commands
import asyncio
from datetime import datetime

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


#別タスクとして投げられるメソッドをすべてこのクラスに格納する
class AsynchronousMethods:
    def set_last_processed(self, d):
        self.last_processed_datadict = d

    async def read_text_loop(self, prompt, max_length):
        await self.sub_obj.send_message(prompt)
        while True:
            # メッセージ応答を待機し、メッセージ、添付ファイル、強制終了フラグを返す。
            msg, _, kill_switch = await self.sub_obj.interrupt_msg_sleep()
            if kill_switch:
                return -1
            
            # if not "" (空文字列)はTrueと評価される。
            if not msg:
                continue

            #passされたときは空のまま何もしない
            if msg == "pass":
                await self.sub_obj.send_message("skipped.")
                break

            #validatorはラムダ式
            #lambda x, y: True if len(x) <= y else False
            #という式を保持している。
            #1, 引数(msg)をlambda xのxとして受け取る。 max_lengthがy。
            #2, 条件式評価し、条件適合（今回は文字数が指定以下）ならそのまま受け取る。
            #Falseであれば再入力を求める。
            if self.validator(msg, max_length):
                return msg
            else:
                await self.sub_obj.send_message(f"{str(max_length)}文字以内で再度入力してください。")
                continue

    async def write_diary(self):
        #validator(評価文字列, 文字数)
        self.validator = lambda x, y: True if len(x) <= y else False

        self.last_processed_datadict = {}
        input_datadict = {
            'title': "",  # <32
            'content': "",  # HTML
            'slug': "",  # <200
            'status': "draft",  # draft=下書き、publish=公開　省略時はdraftになる
        }

        # タイトル入力
        title_prompt = "Please enter a title."
        title = await self.read_text_loop(title_prompt, 32)
        if title == -1:
            self.set_last_processed(input_datadict)
            return
        input_datadict["title"] = title

        # スラッグ入力
        slug_prompt = "Please enter a slug.\n「diary」と入力すると自動で今日の日時[diary-yyyy-mm-dd]となります。"
        slug = await self.read_text_loop(slug_prompt, 200)
        if slug == -1:
            self.set_last_processed(input_datadict)
            return
        if slug == "diary":
            slug = datetime.today().strftime("%Y-%m-%d")
            await self.sub_obj.send_message("slug -> " + slug)
        input_datadict["slug"] = slug
        
        #本文入力
        #embedで各種操作例を表記して入力を開始してもらう。
        embed_text = f"""
            記事は送信ごとに1段落<p>として認識されます。\n
            終始<>であればpタグは省略されます。(回避には開始に\を入れてください。)\n
            一行削除する場合...「undo」\n
            入力を終了する場合...「end」\n
            入力内容確認...「confirm」\n
            行削除...「remove [行番号]or[行番号]-[行番号]」\n
            行追加...「insert [行番号]
            """
        e = self.sub_obj.make_embed("記事の記述", embed_text)
        await self.sub_obj.send_embed(e)


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
        #メッセージを取得したら保持する
        self.got_msg = ""
        self.attachments_list = []

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

    async def on_message(self, message):
        #botと対象チャンネル以外をはじく
        if message.author.bot or message.channel.id != self.channel_id:
            return
        self.got_msg=message.content if message.content != "" else "empty"

        """画像ファイルの処理について
        〇URLを直でブログに貼るか、サーバー上に一時的に保存し添付するか
        決めなければならない
        for attachment in message.attachments:
            if attachment.content_type.startswith('image/'):
                # 画像ファイルを保存する
                await attachment.save(attachment.filename)
                print(f'{attachment.filename}を保存しました')
        """
        
    #メッセージが添付ファイルを受け取ったらそれを返す
    #割りこみを受け取ったら処理する。writingは記事記述中でundoを受け付ける
    async def interrupt_msg_sleep(self, writing=False):
        msg = self.got_msg
        await asyncio.sleep(0.2)

        #割りこみ:強制終了
        if msg.startswith("write_exit"):
            await self.send_message("記述を中断しました。最後に終了した記述は「/resume」で再開できます。")
            return "", [], True
        
        #割りこみ:記事記述中の1行戻る・終了シグナル
        if writing and (msg.startswith("undo") or msg.startswith("end")):
            return msg, [], False

        #ここにメッセージorファイルを受け取ったとき結果を返す
        if self.got_msg != "" or self.attachments_list != []:
            tmp = [self.got_msg, self.attachments_list, False]
            self.got_msg = ""
            self.attachment_list = []
            return tmp
        else:
            return "", [], False

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