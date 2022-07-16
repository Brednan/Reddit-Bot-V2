from bs4 import BeautifulSoup
from requests import Session
import requests


class Account(Session):
    def __init__(self, username, password):
        self.FAILED_LOGIN = 0
        self.NO_CONNECTION = 1
        self.SUCCESSFUL_LOGIN = 2

        Session.__init__(self)

        self.headers_ = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        }

        raw_html_content = self.get('https://www.reddit.com/login', headers=self.headers_).text

        soup = BeautifulSoup(raw_html_content, 'html.parser')

        self.csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

        self.login_payload = {
            'csrf_token': self.csrf_token,
            'otp': '',
            'password': f'{password}',
            'username': f'{username}',
            'dest': 'https://www.reddit.com'
        }

        self.proxy_scheme = {
            'http': 'http://geo.iproyal.com:12323',
            'https': 'http://geo.iproyal.com:12323'
        }

    def login_request(self, timeout):
        attempt = 0

        while True:
            try:
                login_req = self.post(url='https://www.reddit.com/login', data=self.login_payload, headers=self.headers_, cookies=self.cookies, timeout=timeout, proxies=self.proxy_scheme)

                self.headers.update({
                    'x-reddit-loid': login_req.cookies.get('loid')
                })

                print(login_req.headers)

            except requests.exceptions.ConnectionError:
                if attempt >= 3:
                    return self.NO_CONNECTION

                attempt += 1

            else:
                try:
                    if 299 >= login_req.status_code >= 200:
                        return self.SUCCESSFUL_LOGIN

                    else:
                        print(login_req.json())
                        return self.FAILED_LOGIN

                except requests.exceptions.JSONDecodeError:
                    return self.FAILED_LOGIN

                except NameError:
                    return self.FAILED_LOGIN

                except:
                    return self.FAILED_LOGIN

    def downvote_request(self, id_):
        payload = {
            'id': id_,
            'dir': '-1',
            'api_type': 'json'
        }

        self.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'})

        self.get('https://www.reddit.com/r/AuthoritarianMasks/comments/vz2ne5/comment/ig7ezb0/?context=3', proxies=self.proxy_scheme, timeout=5)

        options_ = self.options('https://oauth.reddit.com/api/vote?redditWebClient=desktop2x&app=desktop2x-client-production&raw_json=1&gilding_detail=1', timeout=5, proxies=self.proxy_scheme)

        x_reddit_session = options_.headers.get('x-reddit-session')

        self.headers.update({
            'x-reddit-session': x_reddit_session
        })

        # downvote_result = self.post('https://oauth.reddit.com/api/vote?redditWebClient=desktop2x&app=desktop2x-client-production&raw_json=1&gilding_detail=1', proxies=self.proxy_scheme, data=payload, timeout=5)
        # print(downvote_result.text)
