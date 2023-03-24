import requests

class WpClass:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def test_post(self):
        post_data = {
            'title': '記事投稿テスト',
            'content': '<h2>テストやねん</h2><p>これは、<br>Pythonからの記事投稿の<br>テストです。</p>',
            'slug': 'python-post-test',
            'status': 'draft',  # draft=下書き、publish=公開　省略時はdraftになる
        }
        post_api_url = f'{self.url}/wp-json/wp/v2/posts'
        #json
        response = requests.post(post_api_url, json=post_data, auth=(self.user, self.password))
        p = response.json()
        #"{}".format(json.dumps(p, indent=4))
        return p