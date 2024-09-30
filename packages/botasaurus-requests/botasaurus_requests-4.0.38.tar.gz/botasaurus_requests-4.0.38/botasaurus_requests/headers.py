import os
import re
from os.path import dirname, exists, join
from random import choice as rchoice
from random import randint as rint
from random import randrange as rrange
from typing import Callable, Dict, List, Optional

import httpx
import json
 
def read_json(path):
    with open(path, 'r', encoding="utf-8") as fp:
        data = json.load(fp)
        return data

def read_file(path):
    with open(path, 'r', encoding="utf-8") as fp:
        content = fp.read()
        return content
        
def write_json(data, path):
    with open(path, 'w', encoding="utf-8") as fp:
        json.dump(data, fp)


class OSHeaders:
    @staticmethod
    def windows() -> str:
        version = ('10.0', f'6.{rrange(4)}')[rrange(2)]

        if version == '10.0' or rrange(2):
            version += f"; {('WOW64', 'Win64; x64')[rrange(2)]}"

        return f'Windows NT {version}'

    @staticmethod
    def macos() -> str:
        sub = str(rint(10, 14))
        sub += '_' + str(rint(1, (6 if sub != '14' else 2)))

        return f'Macintosh; Intel Mac OS X 10_{sub}'

    @staticmethod
    def linux() -> str:
        return 'X11; Linux ' + ('x86_64', 'i686', 'i686 on x86_64')[rrange(3)]

    @staticmethod
    def random_os() -> str:
        return (OSHeaders.windows, OSHeaders.macos, OSHeaders.linux)[rrange(3)]()


class VersionScraper:
    threshold: int = 10
    data: List[str]

    @staticmethod
    def leading_num(line: str) -> int:
        return int(line.split('.', 1)[0])

    def __init__(self, force_dl: bool = False) -> None:
        if force_dl or not exists(self.file_name):
            self.data = self.download()
        self.data = self.load()

    def load(self) -> List[str]:
        return read_json(self.file_name)

    def write_file(self, data: List[str]) -> None:
        write_json(data, self.file_name)


class ChromeVersions(VersionScraper):
    resource: str = 'https://raw.githubusercontent.com/vikyd/chromium-history-version-position/master/json/all-version.json'
    file_name: str = join(dirname(__file__), "bin", "CR_VERSIONS.json")

    @staticmethod
    def get_ver(line: str) -> str:
        return re.sub(r'[^\d\.]', '', line)

    def download(self) -> List[str]:
        versions: List[str]
        with httpx.stream('GET', self.resource) as r:
            lines = r.iter_lines()
            # search for first version number
            for line in lines:
                highest_ver = re.search(r'\d+', line)
                if highest_ver:  # on the first number
                    # get leading ver number
                    highest_ver = int(highest_ver[0])
                    break
            # add first item to the versions list
            versions = [self.get_ver(line)]
            # for each line in the stream
            # if the leading number is within 20 of the first number
            # add it to the versions list
            while self.leading_num(versions[-1]) >= highest_ver - self.threshold:
                versions.append(self.get_ver(next(lines)))
        # write the versions list to a file
        self.write_file(versions)
        return versions

    def generate(self) -> str:
        return (
            'Mozilla/5.0 (%PLAT%) AppleWebKit/537.36 (KHTML,'
            + f' like Gecko) Chrome/{rchoice(self.data)} Safari/537.36'
        )


class FirefoxVersions(VersionScraper):
    resource: str = 'https://ftp.mozilla.org/pub/firefox/releases/'
    file_name: str = join(dirname(__file__), "bin", "FF_VERSIONS.json")

    def download(self) -> List[str]:
        resp = httpx.get(self.resource)
        # gather version numbers
        versions: List[str]
        versions = re.findall(r'/pub/firefox/releases/([\d\.]+)/', resp.text)
        versions = sorted(set(versions), key=self.leading_num, reverse=True)

        highest_ver: int = self.leading_num(versions[0])
        # remove versions that have a major number
        # less than the highest version - threshold
        versions = [
            ver for ver in versions if self.leading_num(ver) >= highest_ver - self.threshold
        ]
        self.write_file(versions)
        return versions

    def generate(self) -> str:
        ver: str = rchoice(self.data)
        return f'Mozilla/5.0 (%PLAT%; rv:{ver}) Gecko/20100101 Firefox/{ver}'


if not os.getenv('BOTASAURUS_REQUESTS_MODULE'):
    '''
    Define global `chrome` and `firefox` header generators
    '''
    chrome: Callable = ChromeVersions().generate
    firefox: Callable = FirefoxVersions().generate
    browsers: dict = {'chrome': chrome, 'firefox': firefox}


class Headers:
    '''
    browser - str, chrome/firefox. User Agent browser. Default: random
    os - str, win/mac/lin. OS of User Agent. Default: random
    headers - bool, True/False. Generate random headers or no. Default: False
    '''

    _os: dict = {'win': OSHeaders.windows, 'mac': OSHeaders.macos, 'lin': OSHeaders.linux}

    def __init__(
        self, browser: Optional[str] = None, os: Optional[str] = None, headers: bool = True
    ) -> None:
        self._platform: Callable = self._os.get(os, OSHeaders.random_os)
        self._browser: Callable = browsers.get(browser, (chrome, firefox)[rrange(2)])
        self._headers: bool = headers

    @staticmethod
    def make_header() -> Dict[str, str]:
        return {key: value for key, value in header_template.items() if rrange(2)}

    def generate(self) -> dict:
        platform = self._platform()
        browser = self._browser()

        headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': browser.replace('%PLAT%', platform),
        }

        self._headers and headers.update(self.make_header())

        return headers


header_template: Dict[str, str] = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://google.com',
    'Pragma': 'no-cache',
}
