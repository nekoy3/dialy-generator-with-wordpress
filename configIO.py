# https://github.com/nekoy3/raspi-nfc-bot/blob/main/cfg_rw.py
from getpass import getpass
import configparser
import os

class ConfigClass:
    def create_config(self, config):
        config.read('config.ini', encoding="utf-8_sig")

        config['DISCORD'] = {'guild_id': '', 'channel_id': '', 'token': ''}
        config['WORDPRESS'] = {'url': '', 'username': '', 'api_password': 'console'}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def __init__(self):
        config = configparser.ConfigParser()
        try:
            config.read('config.ini', encoding="utf-8_sig")

            self.guild_id = str(config['DISCORD']['guild_id'])
            self.channel_id = int(config['DISCORD']['channel_id'])
            self.token = str(config['DISCORD']['token'])

            self.url = str(config['WORDPRESS']['url'])
            self.username = str(config['WORDPRESS']['username'])

            p = str(config['WORDPRESS']['api_password'])
            if p == "console":
                self.password = getpass("パスワード")
            else:
                self.password = p

        except Exception as e:
            print("config.iniが存在しないか、設定が間違っています。\n" + str(e))
            # ファイルの存在確認(カレントディレクトリにconfig.iniがあるか)
            if not os.path.isfile('config.ini'):
                self.create_config(config)
            exit()

