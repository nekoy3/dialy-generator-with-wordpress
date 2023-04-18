from configIO import ConfigClass
from connectWP import WpClass
from discordBot import BotClient

#*コンフィグを読み込んでインスタンス化し保持する
#?config.iniを読み込んで項目を保持する。存在しなければ設定を促しプログラムを終了する。
cfg = ConfigClass()

#*WordPress関連の操作を行うインスタンスを生成
wp_client = WpClass(cfg.url, cfg.username, cfg.password)

#*discord botを操作するインスタンスを生成
bot_client = BotClient(cfg.guild_id, cfg.channel_id, wp_client)
print('Starting...')

#*botの実行開始
#!この処理以降は実行されない。
bot_client.run(cfg.token)