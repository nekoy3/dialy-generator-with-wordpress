# daily-generator-bot-with-wordpress  
このdiscord Botは、自身が動作すると同時にWordPressにアクセスし、あらかじめ設定されたdiscordチャンネル上でスラッシュコマンドその他を使用し、簡易的な投稿を実行する事が出来る。  

# 大きな変更点  
- 2023/03/24  
  - 初期ビルド  
- 2023/03/25  
  - 実装機能の構想  
  
# Installation  
適当にどこかのサーバーでconfig.iniに所定事項を記述しbotを稼働させ、discordの該当チャンネル上でwordpressへのログイン処理を行い、正常に動作するかを確認することで稼働できるようになります。  
### Library  
```pip install discord.py```  
(version)  
discord.py v2.0.0  
  
# Usage  
あらかじめ指定されたguildのチャンネルでスラッシュコマンドを打ちこんで記述を開始します。  
コマンドを実行すると対話型で入力要求が開始されるので、手順通りに入力して下さい、  
### 日記
```/write_diary``` 日記の記述を開始  
- 「Please enter a title」 ... タイトル入力  
- 「Please enter a slug」 ... URLのid入力  
  - この2つはpass と入力すると -> 最後に記述します。  
- 「Please enter a content！」 ... 本文を入力  
  - 改行(一行送信)することで次の段落へ行きます。  
  - undo と入力すると前回送信した一行を削除します。  
  - end と入力すると入力完了します。  
  - 文字装飾については後述  
- 「Public?(Y/n)」 ... yでpublic、それ以外はdraft   
- 最後に確認embedが表示されるので、end を入力  
  - edit title/slug/半角英数字 を送信すると次の送信が編集扱いになります。  
  - 半角英数字は段落を示し、行数はembed内で表記されます。  
    - 文字数が多い場合は複数に分解される場合があります。  
- 途中で write_exit を入力すると「本当によろしいですか？(Y/n)」と確認され、yを入力すると記述中の情報を消失し終了します。  
  
### 他ジャンル  
```/write_blog``` 記事の記述を開始  
-  diaryの内容に加えて、タグの付与とカテゴリ入力を求められます。  

- - -
### その他細かい部分  
- 文字の装飾  
  - 未定  
  
# Note  
### カテゴリ入力  
タグとカテゴリ取得については文字列を直指定できない（全てID管理）ので、  
取得 -> embedでid: カテゴリ名 のリストを表示  
参考 https://tkstock.site/2022/01/23/python-wordpress-api-category-list-name-slug/  
/write_blog の時カテゴリ入力を求めるのでid一覧をembedで表示する。  
入力したらembedは削除する。  