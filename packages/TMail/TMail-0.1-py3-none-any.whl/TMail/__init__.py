import requests as r
import string, random, json, time
from bs4 import BeautifulSoup

class TMail:
    host = 'https://tempmail.plus/'
    def __init__(self, name: str = None, domain: str = None, epin: str = None) -> None:
        self.name = name or ''.join(random.sample(string.ascii_letters + string.digits, 6))
        self.av_domain = self.domain_list()
        self.domain = domain or self.av_domain[random.randrange(0, len(self.av_domain)-1)]
        self.epin = epin
        self.email = f'{self.name}@{self.domain}'

    def domain_list(self) -> list:
        source = BeautifulSoup(r.get(self.host).text, 'html.parser')
        domain = [btn.text for btn in source.find('form', id='pre_form').find('div', class_='dropdown-menu').find_all('button')]
        return domain

    def inbox(self) -> json:
        api = r.get(self.host +f'api/mails?email={self.email}&limit=20&epin={self.epin}').json()
        return api
