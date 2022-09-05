from requests_html import HTMLSession
from bs4 import BeautifulSoup
from loguru import logger
import requests
import traceback


class RedditProfile():

    def __init__(self, username: str, password: str, proxy: dict, debug: bool = False) -> None:
        self.session = HTMLSession()
        self.username = username
        self.password = password
        self.token = None
        self.logged = False
        self.debug = debug
        self.proxy = {}
        if False in set([bool(i) for i in list(proxy.values())]):
            self.proxyStr = f"http://{proxy['proxy_user']}:{proxy['proxy_pass']}@{proxy['host']}:{proxy['port']}"
            self.proxy["https"] = self.proxyStr
            self.proxy["http"] = self.proxyStr
        self.session.proxies = self.proxy

    def valid_proxy(self):
        try:
            response_proxy = self.session.get("https://api.ipify.org")
            print(response_proxy.text)
            response_defIp = requests.get("https://api.ipify.org")
            assert response_proxy.text != response_defIp.text
            return True
        except:
            print(traceback.format_exc())
            logger.error(f"Proxy for account {self.username} is not valid!")
            return False
    
    def login(self) -> None:
        if bool(self.proxy):
            if not self.valid_proxy():
                return

        formResponse = self.session.get("https://www.reddit.com/login/")
        soup = BeautifulSoup(formResponse.text, "lxml")

        csrf_token = soup.find("input", {'name': 'csrf_token'})["value"]
        data = {
            "csrf_token": csrf_token,
            'otp': '',
            'password': self.password,
            'dest': 'https://www.reddit.com/',
            'username': self.username,
        }
        r = self.session.post('https://www.reddit.com/login', data=data)
    
        if int(r.status_code) != 200:
            logger.error("Unexpected error occured while logging in")
            return

        self.logged = True

        r = self.session.get("https://www.reddit.com/")

        soup = BeautifulSoup(r.text, "lxml")
        script_block = soup.find("script", {"id": "data"}).text
        list_1 = script_block.split('"')
        self.token = list_1[list_1.index("accessToken") + 2]

        logger.info(f"Successfully logged into reddit account '{self.username}'")

    def vote(self, reddit_post, upvote = True) -> None:
        if (not self.logged) or (not self.token):
            logger.error(f"Can't vote post from account {self.username} because login wasn't done")
            return
        
        temp = reddit_post.split("/")
        postID = temp[temp.index("comments") + 1]
        cookie_dict = self.session.cookies.get_dict()
        params = {
            'redditWebClient': 'desktop2x',
            'app': 'desktop2x-client-production',
            'raw_json': '1',
            'gilding_detail': '1',
        }
        data = {
            'id': f't3_{postID}',
            'dir': '1' if upvote else "-1",
            'api_type': 'json',
        }
        headers = {
            'authority': 'oauth.reddit.com',
            'accept': '*/*',
            'authorization': f'Bearer {self.token}',
            'origin': 'https://www.reddit.com',
            'referer': 'https://www.reddit.com/',
            'x-reddit-loid': cookie_dict['loid'],
            'x-reddit-session': cookie_dict['reddit_session'],
        }
        option_headers = {
            'authority': 'oauth.reddit.com',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'access-control-request-headers': 'authorization,x-reddit-loid,x-reddit-session',
            'access-control-request-method': 'POST',
            'origin': 'https://www.reddit.com',
            'referer': 'https://www.reddit.com/',
        }
        option_params = {
            'redditWebClient': 'desktop2x',
            'app': 'desktop2x-client-production',
            'raw_json': '1',
            'gilding_detail': '1',
        }

        self.session.options('https://oauth.reddit.com/api/vote', params=option_params, headers=option_headers)
        response = self.session.post('https://oauth.reddit.com/api/vote', params=params, data=data, headers=headers)
        
        if int(response.status_code) != 200:
            if upvote:
                logger.error("Unexpected error occured while upvoting the post")
            else:
                logger.error("Unexpected error occured while downvoting the post")
            return
        else:
            if upvote:
                logger.info(f"Reddit post '{postID}' was successfully upvoted from profile '{self.username}'")
            else:
                logger.info(f"Reddit post '{postID}' was successfully downvoted from profile '{self.username}'")
        print(f"Response for vote: {response.text}")
