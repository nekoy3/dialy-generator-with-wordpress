import json
import requests

class WpClass:
    def __init__(self, url, user, password):
        self.post_api_url = f'{url}/wp-json/wp/v2/posts'
        self.user = user
        self.password = password

    def test_post(self) -> json:
        post_data = {
            'title': '記事投稿テスト',
            'content': '<h2>テストやねん</h2><p>これは、<br>Pythonからの記事投稿の<br>テストです。</p>',
            'slug': 'python-post-test',
            'status': 'draft',  # draft=下書き、publish=公開　省略時はdraftになる
        }
        
        #json
        response = requests.post(self.post_api_url, json=post_data, auth=(self.user, self.password))
        p = response.json()
        #"{}".format(json.dumps(p, indent=4))
        return p
    
    def make_post(self, title, content, slug, status="draft") -> dict:
        """
        title: 題名[obj]
        content: 中身[obj]
        slug: 識別子[str]
        status: draft/publish
        """
        post_data = {
            'title': title,
            'content': content,
            'slug': slug,
            'status': status,  # draft=下書き、publish=公開　省略時はdraftになる
        }

        response = requests.post(self.post_api_url, json=post_data, auth=(self.user, self.password))
        p = response.json()