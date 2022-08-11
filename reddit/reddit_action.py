from requests_html import HTMLSession
from bs4 import BeautifulSoup
from loguru import logger


class RedditProfile():

    def __init__(self, username: str, password: str, proxy: dict) -> None:
        self.session = HTMLSession()
        self.username = username
        self.password = password
        self.token = None
        self.logged = False
        self.proxy = {}
        if proxy["host"] != "" and proxy["port"] != "":
            self.proxy["https"] = f"http://{proxy['host']}:{proxy['port']}"
            self.proxy["http"] = f"http://{proxy['host']}:{proxy['port']}"
    
    def login(self) -> None:
        logger.info(f"Logging into reddit account '{self.username}'")
        formResponse = self.session.get("https://www.reddit.com/login/", proxies=self.proxy)
        soup = BeautifulSoup(formResponse.text, "lxml")

        csrf_token = soup.find("input", {'name': 'csrf_token'})["value"]
        data = {
            "csrf_token": csrf_token,
            'otp': '',
            'password': self.password,
            'dest': 'https://www.reddit.com/',
            'username': self.username,
        }
        r = self.session.post('https://www.reddit.com/login', data=data, proxies=self.proxy)

        if int(r.status_code) != 200:
            logger.error("Unexpected error occured while logging in")
            raise "Couldn't login"

        self.logged = True

        r = self.session.get("https://www.reddit.com/", proxies=self.proxy)

        soup = BeautifulSoup(r.text, "lxml")
        script_block = soup.find("script", {"id": "data"}).text
        list_1 = script_block.split('"')
        self.token = list_1[list_1.index("accessToken") + 2]

        logger.info(f"Successfully logged into reddit account '{self.username}'")
        logger.info(f"Bearer token for acc '{self.username}' is '{self.token}'")

    def upvote(self, reddit_post) -> None:
        if (not self.logged) or self.token == None:
            logger.error(f"Can't upvote post from account {self.username} because login wasn't done")
            raise "Can't upvote the post without being logged in"
        
        temp = reddit_post.split("/")
        postID = temp[temp.index("comments") + 1]
        cookie_dict = dict(self.session.cookies)
        params = {
            'redditWebClient': 'desktop2x',
            'app': 'desktop2x-client-production',
            'raw_json': '1',
            'gilding_detail': '1',
        }
        data = {
            'id': f't3_{postID}',
            'dir': '1',
            'api_type': 'json',
        }
        headers = {
            'x-reddit-loid': cookie_dict['loid'],
            'x-reddit-session': cookie_dict['reddit_session'],
            'authorization': f'Bearer {self.token}'
        }

        response = self.session.post('https://oauth.reddit.com/api/vote', params=params, data=data, headers=headers, proxies=self.proxy)

        if int(response.status_code) != 200:
            logger.error("Unexpected error occured while upvoting the post")
            raise "Couldn't upvote the post"
        else:
            logger.info(f"Reddit post '{postID}' was successfully upvoted from profile '{self.username}'")
            
