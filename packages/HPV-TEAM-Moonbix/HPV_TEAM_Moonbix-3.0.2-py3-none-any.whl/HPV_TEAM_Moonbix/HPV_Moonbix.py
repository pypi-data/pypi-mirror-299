from requests import Session, get
from urllib.parse import unquote
from colorama import Fore
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Literal
from os import system as sys, getcwd, path
from platform import system as s_name
from time import sleep, time
from shutil import get_terminal_size as gts
from collections import Counter
from json import dump, dumps, load, loads
from subprocess import run as terminal, Popen
from sys import exit, executable
from secrets import token_hex
from string import ascii_letters as A, digits as D, hexdigits
from uuid import uuid4
from soupsieve.util import lower
from random import uniform, choice, randint, random, choices, shuffle
from base64 import b64encode
from Crypto.Cipher.AES import new as NEW, MODE_CBC as CBC
from Crypto.Random import get_random_bytes as GRB


VERSION = '3.0.2'




















HPV_TEAM = f'''
 _  _ _____   __   __  __               _    _     
| || | _ \ \ / /__|  \/  |___  ___ _ _ | |__(_)_ __
| __ |  _/\ V /___| |\/| / _ \/ _ \ ' \| '_ \ \ \ /
|_||_|_|   \_/    |_|  |_\___/\___/_||_|_.__/_/_\_\\
+-----------------------------------------+
| Контент: t.me/HPV_TEAM /// t.me/HPV_PRO |
+-----------------------------------------+
| Сотрудничество: t.me/HPV_BASE |
+-------------------------------+
| Автор: t.me/A_KTO_Tbl |
+-----------------------+
| V{VERSION} |
+--------+
'''

def HPV_Banner():
    '''Вывод баннера'''

    for HPV in HPV_TEAM.split('\n'): # Вывод баннера
        print(Fore.MAGENTA + HPV.center(gts()[0], ' '))
        sleep(0.026)




















def HPV_Get_Accounts() -> dict:
    '''Получение списка аккаунтов'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Получение списка аккаунтов!')
    PATH = path.join(getcwd(), 'Core', 'Config', 'HPV_Account.json')

    try:
        with open(PATH, 'r') as HPV:
            return load(HPV)
    except:
        print(Fore.MAGENTA + '[HPV]' + Fore.RED + ' — Ошибка чтения `HPV_Account.json`, ссылки указаны некорректно!')
        exit()



def HPV_Get_Proxy() -> list:
    '''Получение списка proxy'''

    PATH = path.join(getcwd(), 'Core', 'Proxy', 'HPV_Proxy.txt')
    PROXY = []

    with open(PATH, 'r') as HPV:
        for Proxy in HPV.read().split('\n'):
            if Proxy:
                try:
                    Proxy = Proxy.split(':')
                    PROXY.append({'IP': Proxy[0], 'Port': Proxy[1], 'Login': Proxy[2], 'Password': Proxy[3]})
                except:
                    pass

        return PROXY



def HPV_Get_Config(_print: bool = True) -> list:
    '''Получение конфигурационных данных'''

    if _print:
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Получение конфигурационных данных!')

    PATH = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.json')

    try:
        with open(PATH, 'r') as HPV:
            return load(HPV)
    except:
        return []



def HPV_Get_Empty_Request() -> dict:
    '''Получение данных c пустыми запросами'''

    try:
        return {
            "Authentication_1": {
                "Method": "get",
                "Url": "https://www.binance.com/game/tg/moon-bix",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "upgrade-insecure-requests": "1", "sec-fetch-site": "none", "sec-fetch-mode": "navigate", "sec-fetch-user": "?1", "sec-fetch-dest": "document", "accept-language": "HPV TEAM"}
            },
            "Authentication_2": {
                "Method": "get",
                "Url": "https://www.binance.com/ru/game/tg/moon-bix",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "upgrade-insecure-requests": "1", "sec-fetch-site": "none", "sec-fetch-mode": "navigate", "sec-fetch-user": "?1", "sec-fetch-dest": "document", "accept-language": "HPV TEAM"}
            },
            "Authentication_3": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/vendor/vendor.umd.0.0.7.production.min.18.2.0.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_4": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/chunks/layout-89a5.7656fe1c.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_5": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/chunks/page-6553.10ad765a.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_6": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/common-widget/vendor@1.3.406.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "style", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_7": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/common-widget/common@1.3.406.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "style", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_8": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/fonts/bp/BinancePlex-Light.woff2",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://www.binance.com", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_9": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/fonts/bp/BinancePlex-Regular.woff2",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://www.binance.com", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_10": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/fonts/bp/BinancePlex-Medium.woff2",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://www.binance.com", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_11": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/fonts/bp/BinancePlex-SemiBold.woff2",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://www.binance.com", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_12": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/runtime/sentry/7.38.0/bundle.es5.min.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_13": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/static/js/telegram-sdk/telegram-web-app.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_14": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/css/2fb8f4a8.chunk.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "style", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_15": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/css/9a46367f.chunk.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "style", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_16": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/css/5d409609.chunk.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "style", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_17": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/fonts/index.min.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "origin": "https://www.binance.com", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "style", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_18": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/fonts/font.min.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "origin": "https://www.binance.com", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "style", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_19": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/js/common-widget/fetch-ponyfill.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_20": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/js/common-widget/tslib.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_21": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/js/common-widget/uuid@9.0.0.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_22": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/js/common-widget/md5.min.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_23": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/js/common-widget/b2a@1.1.2.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_24": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/configs/newbase/com-icon.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_25": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/configs/newbase/common-icon.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_26": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/http/http@1.15.94.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_27": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/themis/themis@0.0.39.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_28": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/common-widget/vendor@1.3.389.min.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_29": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/common-widget/utils@1.3.389.min.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_30": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/common-widget/data@1.3.389.min.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_31": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/common-widget/common@1.3.389.min.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_32": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/web-push-odin/web-push-odin-pre.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_33": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/webpack-runtime.d597ad61.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_34": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/framework.4d1bc876.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_35": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/main.3916b34b.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_36": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/js/common-widget/versionCheck.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_37": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/js/common-widget/extensionRender.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_38": {
                "Method": "get",
                "Url": "https://cdn.cookielaw.org/consent/e21a0e13-40c2-48a6-9ca2-57738356cdab/OtAutoBlock.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_39": {
                "Method": "get",
                "Url": "https://cdn.cookielaw.org/scripttemplates/otSDKStub.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_40": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/one-trust/onetrust-trigger.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_41": {
                "Method": "get",
                "Url": "https://www.googletagmanager.com/gtm.js?id=GTM-M86QHGF",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_42": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/background.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_43": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/astronut.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_44": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/moon.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_45": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/star-blue.gif",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_46": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/star-purple.gif",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_47": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/sfx-confetti.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_48": {
                "Method": "get",
                "Url": "https://cdn.cookielaw.org/consent/e21a0e13-40c2-48a6-9ca2-57738356cdab/e21a0e13-40c2-48a6-9ca2-57738356cdab.json",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_49": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/sensors/sensorsdata@1.26.12.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_50": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/ab22c0e4.775ea5e7.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_51": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/68cdbbdd.e87e200d.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_52": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/6ff8ba64.c397e896.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_53": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/72c8eec2.3fecfa0d.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_54": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/d5ce8a3b.07fc1f29.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_55": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/a12ddacd.c19733bc.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_56": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/10a91914.de05e216.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_57": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/018c49a2.cbe148bc.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_58": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/a486c986.0aa3df08.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_59": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/d0120eb7.a2d2ad9f.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_60": {
                "Method": "get",
                "Url": "https://public.bnbstatic.com/unpkg/monitor/reporter-sdk@2.0.7.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_61": {
                "Method": "get",
                "Url": "https://cdn.cookielaw.org/scripttemplates/202407.2.0/otBannerSdk.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_62": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/chunks/dynamic-analytics-web-vitals.d65ea379.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_63": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/configs/global/common.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_64": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/common/a6d61334.c4f964e0.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_65": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/chunks/dynamic-analytics-utils.c1fe6712.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_66": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/chunks/dynamic-analytics-client-type.166031b8.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_67": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/rms/fc.dyuixccn.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_68": {
                "Method": "get",
                "Url": "https://cdn.cookielaw.org/scripttemplates/202407.2.0/assets/otCommonStyles.css",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_69": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/api/i18n/-/web/cms/ru/growth-game-ui",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_70": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/api/i18n/-/web/cms/ru/growth-platform",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "Authentication_71": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/api/i18n/-/web/cms/ru/widget-common",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },



            "AutoCheckReferrals": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/friends.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },



            "AutoCheckVerif": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/binance-gift.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },



            "AutoGame_1": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/loading-kv.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_2": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/spaceship.png",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_3": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/item-planet.png",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_4": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/item-token.png",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_5": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/item-bonus.png",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_6": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/start-twinkle.png",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_7": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/hook.png",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_8": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/sound/bgm.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_9": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/sound/sfx-claim.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_10": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/sound/sfx-drag.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_11": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/sound/sfx-fire.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_12": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/sound/sfx-gameover.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_13": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/sound/sfx-hititem.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_14": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/sound/sfx-hittrap.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_15": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/game-assets/sound/sfx-timerunningout.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_16": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/icon-timer.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_17": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/icon-score.png",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "origin": "https://www.binance.com", "sec-fetch-site": "cross-site", "sec-fetch-mode": "cors", "sec-fetch-dest": "empty", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_18": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/firework.gif",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            },
            "AutoGame_19": {
                "Method": "get",
                "Url": "https://bin.bnbstatic.com/static/images/activity/crypto-miner/sfx-confetti.mp3",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-site": "cross-site", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "audio", "referer": "https://www.binance.com/", "accept-language": "HPV TEAM"}
            }
        }
    except:
        return {}



def HPV_Get_Accept_Language() -> dict:
    '''Получение данных с языковыми заголовками'''

    try:
        return {
            "RU": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7",
            "US": "en-US,en;q=0.9",
            "GB": "en-GB,en;q=0.9",
            "DE": "de,de-DE;q=0.9,en-US;q=0.8,en;q=0.7",
            "FR": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7",
            "ES": "es,es-ES;q=0.9,en-US;q=0.8,en;q=0.7",
            "IT": "it,it-IT;q=0.9,en-US;q=0.8,en;q=0.7",
            "CN": "zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
            "JP": "ja,ja-JP;q=0.9,en-US;q=0.8,en;q=0.7",
            "KR": "ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7",
            "BR": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "CA": "en-CA,en;q=0.9,fr-CA;q=0.7",
            "AU": "en-AU,en;q=0.9",
            "IN": "en-IN,en;q=0.9,hi;q=0.7",
            "MX": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "NL": "nl,nl-NL;q=0.9,en-US;q=0.8,en;q=0.7",
            "TR": "tr,tr-TR;q=0.9,en-US;q=0.8,en;q=0.7",
            "SE": "sv,sv-SE;q=0.9,en-US;q=0.8,en;q=0.7",
            "NO": "no,no-NO;q=0.9,en;q=0.8",
            "FI": "fi,fi-FI;q=0.9,sv;q=0.8,en;q=0.7",
            "PL": "pl,pl-PL;q=0.9,en-US;q=0.8,en;q=0.7",
            "AR": "es-AR,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "ZA": "en-ZA,en;q=0.9,af;q=0.8,zu;q=0.7",
            "IL": "he,he-IL;q=0.9,en-US;q=0.8,en;q=0.7",
            "EG": "ar,ar-EG;q=0.9,en-US;q=0.8,en;q=0.7",
            "IR": "fa,fa-IR;q=0.9,en-US;q=0.8,en;q=0.7",
            "AF": "fa-AF,ps;q=0.9,en;q=0.8",
            "AL": "sq,sq-AL;q=0.9,en;q=0.8",
            "DZ": "ar-DZ,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "AO": "pt-AO,pt;q=0.9,en;q=0.8",
            "AM": "hy,hy-AM;q=0.9,en;q=0.8",
            "AZ": "az,az-AZ;q=0.9,ru;q=0.8,en;q=0.7",
            "BH": "ar-BH,ar;q=0.9,en;q=0.8",
            "BD": "bn,bn-BD;q=0.9,en;q=0.8",
            "BY": "be,be-BY;q=0.9,ru;q=0.8,en;q=0.7",
            "BE": "nl-BE,fr-BE;q=0.9,de-BE;q=0.8,en;q=0.7",
            "BJ": "fr-BJ,fr;q=0.9,en;q=0.8",
            "BT": "dz,dz-BT;q=0.9,en;q=0.8",
            "BO": "es-BO,es;q=0.9,qu;q=0.8,en;q=0.7",
            "BA": "bs,hr-BA;q=0.9,sr-BA;q=0.8,en;q=0.7",
            "BW": "en-BW,en;q=0.9,tn;q=0.8",
            "BN": "ms-BN,ms;q=0.9,en;q=0.8",
            "BG": "bg,bg-BG;q=0.9,en;q=0.8",
            "BF": "fr-BF,fr;q=0.9,en;q=0.8",
            "BI": "fr-BI,fr;q=0.9,rn;q=0.8,en;q=0.7",
            "KH": "km,km-KH;q=0.9,en;q=0.8",
            "CM": "fr-CM,fr;q=0.9,en-CM;q=0.8,en;q=0.7",
            "CV": "pt-CV,pt;q=0.9,en;q=0.8",
            "TD": "fr-TD,fr;q=0.9,ar-TD;q=0.8,en;q=0.7",
            "CL": "es-CL,es;q=0.9,en;q=0.8",
            "CO": "es-CO,es;q=0.9,en;q=0.8",
            "KM": "fr-KM,fr;q=0.9,ar;q=0.8,en;q=0.7",
            "CG": "fr-CG,fr;q=0.9,en;q=0.8",
            "CD": "fr-CD,fr;q=0.9,en;q=0.8",
            "CR": "es-CR,es;q=0.9,en;q=0.8",
            "CI": "fr-CI,fr;q=0.9,en;q=0.8",
            "HR": "hr,hr-HR;q=0.9,en;q=0.8",
            "CU": "es-CU,es;q=0.9,en;q=0.8",
            "CY": "el-CY,el;q=0.9,tr;q=0.8,en;q=0.7",
            "CZ": "cs,cs-CZ;q=0.9,en;q=0.8",
            "DK": "da,da-DK;q=0.9,en;q=0.8",
            "DJ": "fr-DJ,fr;q=0.9,ar-DJ;q=0.8,en;q=0.7",
            "DO": "es-DO,es;q=0.9,en;q=0.8",
            "EC": "es-EC,es;q=0.9,en;q=0.8",
            "SV": "es-SV,es;q=0.9,en;q=0.8",
            "GQ": "es-GQ,es;q=0.9,fr;q=0.8,pt;q=0.7",
            "ER": "ti,ti-ER;q=0.9,ar;q=0.8,en;q=0.7",
            "EE": "et,et-EE;q=0.9,ru;q=0.8,en;q=0.7",
            "SZ": "en-SZ,en;q=0.9,ss;q=0.8",
            "ET": "am,am-ET;q=0.9,en;q=0.8",
            "FJ": "en-FJ,en;q=0.9,fj;q=0.8",
            "GA": "fr-GA,fr;q=0.9,en;q=0.8",
            "GM": "en-GM,en;q=0.9",
            "GE": "ka,ka-GE;q=0.9,ru;q=0.8,en;q=0.7",
            "GH": "en-GH,en;q=0.9",
            "GR": "el,el-GR;q=0.9,en;q=0.8",
            "GT": "es-GT,es;q=0.9,en;q=0.8",
            "GN": "fr-GN,fr;q=0.9,en;q=0.8",
            "GW": "pt-GW,pt;q=0.9,en;q=0.8",
            "GY": "en-GY,en;q=0.9",
            "HT": "fr-HT,fr;q=0.9,ht;q=0.8,en;q=0.7",
            "HN": "es-HN,es;q=0.9,en;q=0.8",
            "HU": "hu,hu-HU;q=0.9,en;q=0.8",
            "IS": "is,is-IS;q=0.9,en;q=0.8",
            "ID": "id,id-ID;q=0.9,en;q=0.8",
            "IQ": "ar-IQ,ar;q=0.9,ku;q=0.8,en;q=0.7",
            "IE": "en-IE,en;q=0.9,ga;q=0.8",
            "JM": "en-JM,en;q=0.9",
            "JO": "ar-JO,ar;q=0.9,en;q=0.8",
            "KZ": "kk,kk-KZ;q=0.9,ru;q=0.8,en;q=0.7",
            "KE": "en-KE,en;q=0.9,sw;q=0.8",
            "KI": "en-KI,en;q=0.9",
            "KP": "ko-KP,ko;q=0.9,en;q=0.8",
            "KW": "ar-KW,ar;q=0.9,en;q=0.8",
            "KG": "ky,ky-KG;q=0.9,ru;q=0.8,en;q=0.7",
            "LA": "lo,lo-LA;q=0.9,en;q=0.8",
            "LV": "lv,lv-LV;q=0.9,ru;q=0.8,en;q=0.7",
            "LB": "ar-LB,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "LS": "en-LS,en;q=0.9,st;q=0.8",
            "LR": "en-LR,en;q=0.9",
            "LY": "ar-LY,ar;q=0.9,en;q=0.8",
            "LI": "de-LI,de;q=0.9,en;q=0.8",
            "LT": "lt,lt-LT;q=0.9,ru;q=0.8,en;q=0.7",
            "LU": "fr-LU,fr;q=0.9,de;q=0.8,en;q=0.7",
            "MG": "mg,mg-MG;q=0.9,fr;q=0.8,en;q=0.7",
            "MW": "en-MW,en;q=0.9,ny;q=0.8",
            "MY": "ms,my-MY;q=0.9,en;q=0.8",
            "MV": "dv,dv-MV;q=0.9,en;q=0.8",
            "ML": "fr-ML,fr;q=0.9,en;q=0.8",
            "MT": "mt,mt-MT;q=0.9,en;q=0.8",
            "MR": "ar-MR,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "MU": "en-MU,en;q=0.9,fr;q=0.8",
            "MN": "mn,mn-MN;q=0.9,ru;q=0.8,en;q=0.7",
            "ME": "sr-ME,sr;q=0.9,bs;q=0.8,en;q=0.7",
            "MA": "ar-MA,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "MZ": "pt-MZ,pt;q=0.9,en;q=0.8",
            "MM": "my,my-MM;q=0.9,en;q=0.8",
            "NA": "en-NA,en;q=0.9,af;q=0.8,de;q=0.7",
            "NP": "ne,np;q=0.9,en;q=0.8",
            "NZ": "en-NZ,en;q=0.9,mi;q=0.8",
            "NI": "es-NI,es;q=0.9,en;q=0.8",
            "NE": "fr-NE,fr;q=0.9,en;q=0.8",
            "NG": "en-NG,en;q=0.9,yo;q=0.8,ha;q=0.7",
            "MK": "mk,mk-MK;q=0.9,sq;q=0.8,en;q=0.7",
            "OM": "ar-OM,ar;q=0.9,en;q=0.8",
            "PK": "ur,ur-PK;q=0.9,en;q=0.8",
            "PA": "es-PA,es;q=0.9,en;q=0.8",
            "PG": "en-PG,en;q=0.9,tpi;q=0.8",
            "PY": "es-PY,es;q=0.9,gn;q=0.8,en;q=0.7",
            "PE": "es-PE,es;q=0.9,qu;q=0.8,en;q=0.7",
            "PH": "en-PH,en;q=0.9,tl;q=0.8",
            "PT": "pt-PT,pt;q=0.9,en;q=0.8",
            "QA": "ar-QA,ar;q=0.9,en;q=0.8",
            "RO": "ro,ro-RO;q=0.9,en;q=0.8",
            "RW": "rw,rw-RW;q=0.9,fr;q=0.8,en;q=0.7",
            "KN": "en-KN,en;q=0.9",
            "LC": "en-LC,en;q=0.9",
            "VC": "en-VC,en;q=0.9",
            "WS": "sm,sm-WS;q=0.9,en;q=0.8",
            "ST": "pt-ST,pt;q=0.9,en;q=0.8",
            "SA": "ar-SA,ar;q=0.9,en;q=0.8",
            "SN": "fr-SN,fr;q=0.9,en;q=0.8",
            "SC": "fr-SC,fr;q=0.9,en;q=0.8",
            "SL": "en-SL,en;q=0.9",
            "SG": "en-SG,en;q=0.9,zh;q=0.8,ms;q=0.7",
            "SB": "en-SB,en;q=0.9",
            "SO": "so,so-SO;q=0.9,en;q=0.8",
            "SS": "en-SS,en;q=0.9,ar;q=0.8",
            "SD": "ar-SD,ar;q=0.9,en;q=0.8",
            "SR": "nl-SR,nl;q=0.9,en;q=0.8",
            "SY": "ar-SY,ar;q=0.9,en;q=0.8",
            "TJ": "tg,tg-TJ;q=0.9,ru;q=0.8,en;q=0.7",
            "TZ": "sw-TZ,sw;q=0.9,en;q=0.8",
            "TH": "th,th-TH;q=0.9,en;q=0.8",
            "TL": "pt-TL,pt;q=0.9,en;q=0.8",
            "TG": "fr-TG,fr;q=0.9,en;q=0.8",
            "TO": "to,to-TO;q=0.9,en;q=0.8",
            "TT": "en-TT,en;q=0.9,hns;q=0.8,fr;q=0.7",
            "TN": "ar-TN,ar;q=0.9,fr;q=0.8,en;q=0.7",
            "TM": "tk,tk-TM;q=0.9,ru;q=0.8,en;q=0.7",
            "TV": "en-TV,en;q=0.9",
            "UG": "en-UG,en;q=0.9,sw;q=0.8",
            "AE": "ar-AE,ar;q=0.9,en;q=0.8",
            "UY": "es-UY,es;q=0.9,en;q=0.8",
            "UZ": "uz,uz-UZ;q=0.9,ru;q=0.8,en;q=0.7",
            "VU": "bi,bi-VU;q=0.9,en;q=0.8,fr;q=0.7",
            "VA": "it-VA,it;q=0.9,en;q=0.8",
            "VE": "es-VE,es;q=0.9,en;q=0.8",
            "VN": "vi,vi-VN;q=0.9,en;q=0.8",
            "YE": "ar-YE,ar;q=0.9,en;q=0.8",
            "ZM": "en-ZM,en;q=0.9",
            "ZW": "en-ZW,en;q=0.9,sn;q=0.8"
        }
    except:
        return {}










def HPV_Request(proxy: dict) -> bool:
    try:
        get('https://ipecho.net/plain', proxies=proxy)
        return True
    except:
        return False



def HPV_Checker(proxy) -> dict:
    PROXY = f"{proxy['Login']}:{proxy['Password']}@{proxy['IP']}:{proxy['Port']}"
    PROXY_HTTPS = {'http': f'http://{PROXY}', 'https': f'https://{PROXY}'}
    PROXY_SOCKS5 = {'http': f'socks5://{PROXY}', 'https': f'socks5://{PROXY}'}

    if HPV_Request(PROXY_HTTPS):
        return PROXY_HTTPS
    elif HPV_Request(PROXY_SOCKS5):
        return PROXY_SOCKS5



def HPV_Proxy_Checker(_print: bool = True) -> list:
    '''Проверка HTTPS, SOCKS5 проксей на валидность'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Получение списка проксей!') if _print else None
    PROXY_LIST = HPV_Get_Proxy() # Список всех доступных проксей с файла
    VALID_PROXY = [] # Список валидных проксей
    THREADS = [] # Список потоков

    if PROXY_LIST:
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка прокси на работоспособность... Подождите немного!') if _print else None

        def _HPV_Checker(proxy):
            HPV = HPV_Checker(proxy)
            if HPV:
                VALID_PROXY.append(HPV)

        for proxy in PROXY_LIST:
            THREAD = Thread(target=_HPV_Checker, args=(proxy,))
            THREAD.start()
            THREADS.append(THREAD)

        for THREAD in THREADS:
            THREAD.join()

        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + f' — Проверка прокси окончена! Работоспособные: {len(VALID_PROXY)}') if _print else None
    
    else:
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Прокси не обнаружены!') if _print else None

    return VALID_PROXY









def Device_Info(
    SCREEN: str,
    WINDOWS: str,
    BRAND_MODEL: str,
    SYSTEM_LANGUAGE: str,
    TIME_ZONE: str,
    TIME_ZONE_OFFSET: int,
    USER_AGENT: str,
    CANVAS_CODE: str,
    WEBGL_VENDOR: str,
    WEBGL_RENDERER: str,
    AUDIO: str,
    TIME_ZONE_WEB: str,
    FINGERPRINT: str
    ) -> str:
    '''Генерация данных уникального устройства'''

    HPV = dumps({
        'screen_resolution': SCREEN,
        'available_screen_resolution': SCREEN,
        'system_version': WINDOWS,
        'brand_model': BRAND_MODEL,
        'system_lang': SYSTEM_LANGUAGE,
        'timezone': TIME_ZONE,
        'timezoneOffset': TIME_ZONE_OFFSET,
        'user_agent': USER_AGENT,
        'list_plugin': '',
        'canvas_code': CANVAS_CODE,
        'webgl_vendor': WEBGL_VENDOR,
        'webgl_renderer': WEBGL_RENDERER,
        'audio': AUDIO,
        'platform': 'Win64',
        'web_timezone': TIME_ZONE_WEB,
        'device_name': f'{USER_AGENT} (Windows)',
        'fingerprint': FINGERPRINT,
        'device_id': '',
        'related_device_ids': ''
    })

    return b64encode(HPV.encode()).decode()

def HPV_Headers() -> dict:
    '''Генератор уникальных параметров для Headers'''

    HPV_BRAND_MODEL = [

    # Dell
    'Dell XPS 13 Plus',
    'Dell XPS 17',
    'Dell Inspiron 16 Plus',
    'Dell Latitude 9430',
    'Dell G15 Gaming',

    # HP
    'HP Spectre x360 14',
    'HP Envy x360 15',
    'HP Pavilion Plus 14',
    'HP Omen 16',
    'HP Elite Dragonfly G3',

    # Lenovo
    'Lenovo ThinkPad X1 Carbon',
    'Lenovo Yoga 9i',
    'Lenovo Legion 7i',
    'Lenovo ThinkBook 16p',
    'Lenovo IdeaPad Gaming 3i',

    # Acer
    'Acer Swift Edge',
    'Acer Predator Helios 300',
    'Acer Aspire Vero',
    'Acer Spin 5',
    'Acer Nitro 5',

    # Asus
    'Asus ZenBook Pro Duo 14',
    'Asus ROG Zephyrus G14',
    'Asus TUF Gaming F15',
    'Asus VivoBook S14X OLED',
    'Asus ExpertBook B9',

    # MSI
    'MSI Stealth 15M',
    'MSI Raider GE77 HX',
    'MSI Creator Z17',
    'MSI Prestige 14 Evo',
    'MSI Katana GF66',

    # Samsung
    'Samsung Galaxy Book2 Pro',
    'Samsung Galaxy Book2 360',
    'Samsung Galaxy Book3 Ultra',
    'Samsung Galaxy Book2 Business',
    'Samsung Galaxy Book2 Go 5G',

    # Huawei
    'Huawei MateBook X Pro',
    'Huawei MateBook D 16',
    'Huawei MateBook 14s',
    'Huawei MateBook E',

    # Sony (VAIO)
    'Sony VAIO Z',
    'Sony VAIO SX14',
    'Sony VAIO FE14'

]
    HPV_CHROME_VERSION = [

        '129.0.6668.59',  # 18 сен 2024
        '128.0.6613.138', # 11 сен 2024
        '128.0.6613.120', # 3 сен 2024
        '128.0.6613.85',  # 22 авг 2024
        '127.0.6533.120', # 14 авг 2024
        '127.0.6533.100', # 7 авг 2024
        '127.0.6533.89',  # 31 июл 2024
        '127.0.6533.73',  # 24 июл 2024
        '126.0.6478.183', # 17 июл 2024
        '128.0.6537.0',   # 25 июн 2024
        '126.0.6478.115', # 19 июн 2024
        '126.0.6478.62',  # 18 июн 2024
        '126.0.6478.57',  # 12 июн 2024
        '125.0.6422.142', # 31 мая 2024
        '125.0.6422.77',  # 22 мая 2024
        '124.0.6367.207', # 14 мая 2024
        '124.0.6367.119', # 1 мая 2024
        '124.0.6367.92',  # 26 апр 2024
        '124.0.6367.61',  # 17 апр 2024
        '123.0.6312.123', # 12 апр 2024
        '123.0.6312.106', # 3 апр 2024

    ]
    HPV_EDGE_VERSION = [

        '129.0.2792.52',  # 20 сен 2024
        '128.0.2739.79',  # 18 сен 2024
        '128.0.2739.67',  # 11 сен 2024
        '128.0.2739.63',  # 4 сен 2024
        '128.0.2739.54',  # 2 сен 2024
        '127.0.2651.98',  # 12 авг 2024
        '127.0.2651.86',  # 6 авг 2024
        '126.0.2592.87',  # 3 июл 2024
        '126.0.2592.68',  # 21 июн 2024
        '125.0.2535.92',  # 12 июн 2024
        '125.0.2535.85',  # 5 июн 2024
        '124.0.2478.67',  # 1 мая 2024

    ]
    HPV_LOCATION = [

        {
            'System_Language': 'ru-RU',  # Русский
            'Language': 'ru',
            'Time_Zone': 'GMT+03:00',
            'Time_Zone_Offset': 180,
            'Time_Zone_Web': 'Europe/Moscow'
        },
        {
            'System_Language': 'en-EN',  # Английский (США)
            'Language': 'en',
            'Time_Zone': 'GMT-05:00',
            'Time_Zone_Offset': -300,
            'Time_Zone_Web': 'America/New_York'
        },
        {
            'System_Language': 'uz-UZ',  # Узбекский
            'Language': 'ru',
            'Time_Zone': 'GMT+05:00',
            'Time_Zone_Offset': 300,
            'Time_Zone_Web': 'Asia/Tashkent'
        },
        {
            'System_Language': 'kk-KZ',  # Казахский
            'Language': 'ru',
            'Time_Zone': 'GMT+06:00',
            'Time_Zone_Offset': 360,
            'Time_Zone_Web': 'Asia/Almaty'
        },
        {
            'System_Language': 'fr-FR',  # Французский
            'Language': 'en',
            'Time_Zone': 'GMT+01:00',
            'Time_Zone_Offset': 60,
            'Time_Zone_Web': 'Europe/Paris'
        },
        {
            'System_Language': 'de-DE',  # Немецкий
            'Language': 'en',
            'Time_Zone': 'GMT+01:00',
            'Time_Zone_Offset': 60,
            'Time_Zone_Web': 'Europe/Berlin'
        },
        {
            'System_Language': 'es-ES',  # Испанский
            'Language': 'en',
            'Time_Zone': 'GMT+01:00',
            'Time_Zone_Offset': 60,
            'Time_Zone_Web': 'Europe/Madrid'
        },
        {
            'System_Language': 'zh-CN',  # Китайский (упрощенный)
            'Language': 'en',
            'Time_Zone': 'GMT+08:00',
            'Time_Zone_Offset': 480,
            'Time_Zone_Web': 'Asia/Shanghai'
        },
        {
            'System_Language': 'ja-JP',  # Японский
            'Language': 'en',
            'Time_Zone': 'GMT+09:00',
            'Time_Zone_Offset': 540,
            'Time_Zone_Web': 'Asia/Tokyo'
        },
        {
            'System_Language': 'ko-KR',  # Корейский
            'Language': 'en',
            'Time_Zone': 'GMT+09:00',
            'Time_Zone_Offset': 540,
            'Time_Zone_Web': 'Asia/Seoul'
        },
        {
            'System_Language': 'it-IT',  # Итальянский
            'Language': 'en',
            'Time_Zone': 'GMT+01:00',
            'Time_Zone_Offset': 60,
            'Time_Zone_Web': 'Europe/Rome'
        },
        {
            'System_Language': 'pt-PT',  # Португальский
            'Language': 'en',
            'Time_Zone': 'GMT+00:00',
            'Time_Zone_Offset': 0,
            'Time_Zone_Web': 'Europe/Lisbon'
        },
        {
            'System_Language': 'tr-TR',  # Турецкий
            'Language': 'en',
            'Time_Zone': 'GMT+03:00',
            'Time_Zone_Offset': 180,
            'Time_Zone_Web': 'Europe/Istanbul'
        },
        {
            'System_Language': 'ar-SA',  # Арабский
            'Language': 'en',
            'Time_Zone': 'GMT+03:00',
            'Time_Zone_Offset': 180,
            'Time_Zone_Web': 'Asia/Riyadh'
        }

    ]
    HPV_SCREEN = [

        '1280,720',  # HD (16:9)
        '1280,800',  # WXGA
        '1366,768',  # HD (более распространенное)
        '1440,900',  # WXGA+
        '1600,900',  # HD+
        '1680,1050', # WSXGA+
        '1920,1080', # Full HD
        '1920,1200', # WUXGA
        '2048,1080', # 2K (DCI)
        '2160,1440', # 3:2 (Surface и подобное)
        '2560,1440', # QHD
        '2560,1600', # WQXGA
        '2880,1800', # Retina MacBook Pro 15'
        '3200,1800', # QHD+
        '3440,1440', # UltraWide QHD (21:9)
        '3840,2160', # 4K UHD
        '4096,2160', # 4K DCI
        '1280,1024', # SXGA
        '1360,768',  # HD (иногда используется на ноутбуках)
        '1440,2560', # WQHD
        '1600,1200', # UXGA
        '1920,1440', # QUXGA
        '2048,1536', # QXGA
        '2560,2048', # QSXGA
        '3200,2400', # QUXGA
        '3840,2400', # WQUXGA
        '1280,960',  # SXGA-
        '1600,768',  # UWHD
        '1440,1080', # Fullscreen XGA
        '3440,1440', # UWQHD
        '1366,1024', # HD+ (4:3, иногда встречается)
        '2560,1080', # UWHD (21:9)
        '1792,1344', # Super-XGA+
        '3200,2000', # WQXGA+
        '2880,1620'  # QHD+ (3:2, на некоторых ноутбуках)

    ]
    HPV_WINDOWS_VERSIONS = [

        'Windows 10 Home',
        'Windows 10 Pro',
        'Windows 10 Enterprise',
        'Windows 10 Education',
        'Windows 10 Pro for Workstations',
        'Windows 11 Home',
        'Windows 11 Pro',
        'Windows 11 Enterprise',
        'Windows 11 Education',
        'Windows 11 Pro for Workstations',
        'Windows 11 SE'

    ]

    def HPV_WEBGL() -> dict:
        '''Генератор параметров WebGL'''

        VENDORS_AND_RENDERERS = {

            'Intel': [
                'Intel(R) HD Graphics 520', 
                'Intel(R) HD Graphics 530',
                'Intel(R) HD Graphics 620',
                'Intel(R) HD Graphics 630',
                'Intel(R) UHD Graphics 600',
                'Intel(R) UHD Graphics 605',
                'Intel(R) UHD Graphics 620',
                'Intel(R) Iris Plus Graphics 640',
                'Intel(R) Iris Plus Graphics 650',
                'Intel(R) Iris Xe Graphics'
            ],

            'NVIDIA': [
                'NVIDIA GeForce GTX 1050',
                'NVIDIA GeForce GTX 1050 Ti',
                'NVIDIA GeForce GTX 1060',
                'NVIDIA GeForce GTX 1070',
                'NVIDIA GeForce GTX 1080',
                'NVIDIA GeForce GTX 1650',
                'NVIDIA GeForce GTX 1660',
                'NVIDIA GeForce RTX 2060',
                'NVIDIA GeForce RTX 2070',
                'NVIDIA GeForce RTX 2080',
                'NVIDIA GeForce RTX 3060',
                'NVIDIA GeForce RTX 3070',
                'NVIDIA GeForce RTX 3080',
                'NVIDIA GeForce RTX 3090',
                'NVIDIA GeForce MX250',
                'NVIDIA GeForce MX330',
                'NVIDIA GeForce MX450'
            ],

            'AMD': [
                'AMD Radeon RX 560',
                'AMD Radeon RX 570',
                'AMD Radeon RX 580',
                'AMD Radeon RX 590',
                'AMD Radeon RX 6600',
                'AMD Radeon RX 6700 XT',
                'AMD Radeon RX 6800',
                'AMD Radeon RX 6800 XT',
                'AMD Radeon RX 6900 XT',
                'AMD Radeon Vega 8',
                'AMD Radeon Vega 10',
                'AMD Radeon RX Vega 56',
                'AMD Radeon RX Vega 64'
            ]

        }
        RENDERING_TECHNOLOGIES = [

            'Direct3D11',
            'OpenGL',
            'Vulkan'

    ]

        WEBGL_VENDOR = choice(list(VENDORS_AND_RENDERERS.keys())) # Случайный производитель
        GPU_MODEL = choice(VENDORS_AND_RENDERERS[WEBGL_VENDOR]) # Случайная GPU, соответствующая производителю
        WEBGL_RENDERER = f'ANGLE ({WEBGL_VENDOR}, {GPU_MODEL} {choice(RENDERING_TECHNOLOGIES)} vs_5_0 ps_5_0)'

        return {'WEBGL_VENDOR': WEBGL_VENDOR, 'WEBGL_RENDERER': WEBGL_RENDERER}


    UUID = str(uuid4()) # UUID
    WINDOWS = choice(HPV_WINDOWS_VERSIONS) # Версии Windows
    CHROME = choice(HPV_CHROME_VERSION) # Версия Google Chrome
    EDGE = choice((HPV_EDGE_VERSION)) # Версия Microsoft Edge

    USER_AGENT = f'Mozilla/5.0 ({WINDOWS}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{CHROME} Safari/537.36 Edg/{EDGE}'
    SEC_CH_UA = f'"Microsoft Edge";v="{EDGE.split(".")[0]}", "Not(A:Brand";v="8", "Chromium";v="{CHROME.split(".")[0]}", "Microsoft Edge WebView2";v="{EDGE.split(".")[0]}"'

    SCREEN = choice(HPV_SCREEN) # Разрешение экрана
    BRAND_MODEL = choice(HPV_BRAND_MODEL) # Модель ноутбука или компьютера

    HPV_Location = choice(HPV_LOCATION)
    SYSTEM_LANGUAGE = HPV_Location['System_Language'] # Язык системы
    LANGUAGE = HPV_Location['Language'] # Язык
    TIME_ZONE = HPV_Location['Time_Zone'] # GMT
    TIME_ZONE_OFFSET = HPV_Location['Time_Zone_Offset'] # Смещение времени
    TIME_ZONE_WEB = HPV_Location['Time_Zone_Web'] # Часовой пояс

    CANVAS_CODE = ''.join(choices(lower(hexdigits), k=8))

    HPV_WebGL = HPV_WEBGL()
    WEBGL_VENDOR = HPV_WebGL['WEBGL_VENDOR'] # Производитель
    WEBGL_RENDERER = HPV_WebGL['WEBGL_RENDERER'] # WebGL GPU

    AUDIO = str(uniform(100, 130))
    FINGERPRINT = ''.join(choices(lower(hexdigits), k=32))

    DEVICE_INFO = Device_Info(SCREEN, WINDOWS, BRAND_MODEL, SYSTEM_LANGUAGE, TIME_ZONE, TIME_ZONE_OFFSET, USER_AGENT, CANVAS_CODE, WEBGL_VENDOR, WEBGL_RENDERER, AUDIO, TIME_ZONE_WEB, FINGERPRINT)

    return {
        'UUID': UUID, 'WINDOWS': WINDOWS, 'USER_AGENT': USER_AGENT, 'SEC_CH_UA': SEC_CH_UA, 'SCREEN': SCREEN, 'BRAND_MODEL': BRAND_MODEL,
        'SYSTEM_LANGUAGE': SYSTEM_LANGUAGE, 'LANGUAGE': LANGUAGE, 'TIME_ZONE': TIME_ZONE, 'TIME_ZONE_OFFSET': TIME_ZONE_OFFSET,
        'TIME_ZONE_WEB': TIME_ZONE_WEB, 'CANVAS_CODE': CANVAS_CODE, 'WEBGL_VENDOR': WEBGL_VENDOR, 'WEBGL_RENDERER': WEBGL_RENDERER,
        'AUDIO': AUDIO, 'FINGERPRINT': FINGERPRINT, 'DEVICE_INFO': DEVICE_INFO
        }




















def HPV_Config_Setup() -> None:
    '''Настройка конфига'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Настройка конфига... Подождите немного!')
    Accounts = HPV_Get_Accounts() # Словарь аккаунтов

    if Accounts:
        Proxys = HPV_Proxy_Checker() # Список проксей
        User_Agents = [] # Список уникальных параметров для Headers
        Uniq = [] # Список с уникальными параметрами для каждого аккаунта


        # Генератор уникальных параметров для Headers в количестве, соответствующем числу аккаунтов
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Генерация уникальных параметров Headers для каждого аккаунта!')
        while len(User_Agents) < len(Accounts):
            Headers = HPV_Headers() # Новые сгенерированные параметры для Headers
            if Headers not in User_Agents: # Проверка на отсутствие таких же параметров для Headers
                User_Agents.append(Headers)


        # Создание уникальных личностей для каждого аккаунта
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Создание уникальных личностей для каждого аккаунта!')
        for Number, Key in enumerate(Accounts):
            Uniq.append({'Name': Key, 'URL': Accounts[Key], 'Proxy': Proxys[Number % len(Proxys)] if len(Proxys) > 0 else None, 'Headers': User_Agents[Number]})


        # Сохранение данных
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Сохранение конфигурационных данных!')
        PATH = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.json')
        with open(PATH, 'w', encoding='utf-8') as HPV:
            dump(Uniq, HPV, ensure_ascii=False, indent=4)

    else:
        print(Fore.MAGENTA + '[HPV]' + Fore.YELLOW + ' — Аккаунты не найдены!')
        exit()











def HPV_Upgrade_Alert(AUTO_UPDATE) -> bool:
    '''Проверка наличия обновления'''

    try:
        if AUTO_UPDATE:
            HPV = get('https://pypi.org/pypi/HPV-TEAM-Moonbix/json').json()['info']['version']
            return True if VERSION < HPV else False
    except:
        return False



def HPV_Upgrade(AUTO_UPDATE) -> None:
    '''Автоматическая проверка и установка обновления'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка наличия обновления... Подождите немного!')
    PIP = 'pip' if s_name() == 'Windows' else 'pip3' # Определение ОС, для установки зависимостей

    try:
        if HPV_Upgrade_Alert(AUTO_UPDATE):
            print(Fore.MAGENTA + '[HPV]' + Fore.YELLOW + ' — Обнаружено обновление!')

            if AUTO_UPDATE:
                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Идёт процесс обновления... Подождите немного!')
                terminal([PIP, 'install', '--upgrade', 'HPV_TEAM_Moonbix'], check=True) # Установка зависимостей

                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Перезапуск программы...')
                Popen([executable, path.join(getcwd(), 'HPV_Moonbix.py')]); exit() # Перезапуск программы

            else:
                print(Fore.MAGENTA + '[HPV]' + Fore.YELLOW + ' — Автообновления отключены! Обновление не установлено!')

        else:
            print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Обновлений не обнаружено!')

    except Exception as ERROR:
        print(Fore.MAGENTA + '[HPV]' + Fore.RED + f' — Что-то пошло не так!\n\tОшибка: {ERROR}')








def HPV_Checking(File: str, Content: str) -> bool:
    '''Создание конфигурационных файлов'''

    try:
        with open(File, 'w') as HPV:
            if File.endswith('.json'):
                dump(Content, HPV, indent=4)
            else:
                HPV.write(Content)
    except:
        pass



def HPV_Check_Configs():
    '''Проверка наличия конфигурационных файлов'''

    HPV_Account_json = path.join(getcwd(), 'Core', 'Config', 'HPV_Account.json')
    HPV_Config_json = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.json')
    HPV_Config_py = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.py')
    HPV_Proxy_txt = path.join(getcwd(), 'Core', 'Proxy', 'HPV_Proxy.txt')

    FILES = {
        HPV_Account_json: {'ACCOUNT_1': 'https://www.binance.com/game/tg/moon-bix#tgWebAppData=...', 'ACCOUNT_2': 'https://www.binance.com/game/tg/moon-bix#tgWebAppData=...'},
        HPV_Config_json: '',
        HPV_Config_py: '\n\n# Автоматическое обновление программы\nAUTO_UPDATE = True # Для включения установите значение True, для отключения — False.\n# По умолчанию автообновление включено, и рекомендуется не изменять этот параметр. Однако, вы можете его отключить по соображениям безопасности!\n\n',
        HPV_Proxy_txt: ''
    }

    for File, Content in FILES.items():
        if not path.exists(File):
            HPV_Checking(File, Content)



def HPV_Config_Check(AUTO_UPDATE) -> None:
    '''Проверка конфига на валидность'''

    print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка конфига... Подождите немного!')
    HPV_Check_Configs() # Проверка наличия конфигурационных файлов
    HPV_Upgrade(AUTO_UPDATE) # Автоматическая проверка и установка обновления
    Config = HPV_Get_Config() # Получение конфигурационных данных

    if Config:
        Accounts = HPV_Get_Accounts() # Получение списка аккаунтов
        ALL_PROXY = HPV_Proxy_Checker(_print=False) # Список всех доступных проксей
        USE_PROXY = [Proxy['Proxy'] for Proxy in Config] # Список используемых проксей
        INVALID_PROXY = [] # Список невалидных проксей

        USE_HEADERS = [Headers['Headers'] for Headers in Config] # Список используемых параметров для Headers

        THREADS = [] # Список потоков
        NEW_CONFIG = [] # Данные нового конфига, в случае изменений
        CHANGES = False # Были / небыли изменения


        # Проверка проксей каждой личности
        def HPV_Proxy_Check(Proxy) -> None:
            if not HPV_Request(Proxy):
                INVALID_PROXY.append(Proxy)


        # Получение свободного или малоиспользуемого прокси
        def HPV_New_Proxy():
            if FREE_PROXY: # Если есть свободные прокси из всего списка
                return FREE_PROXY.pop(0) # Берётся первый свободный прокси
            else: # Если свободных проксей нет
                USE_PROXY_COUNTER = Counter([dumps(_PROXY, sort_keys=True) for _PROXY in USE_PROXY])
                LEAST_USED_PROXY = loads(min(USE_PROXY_COUNTER, key=USE_PROXY_COUNTER.get))
                USE_PROXY.append(LEAST_USED_PROXY)
                return LEAST_USED_PROXY


        # Генерация новых параметров для Headers
        def HPV_New_Headers():
            while True:
                Headers = HPV_Headers() # Новые сгенерированные параметры для Headers
                if Headers not in USE_HEADERS:
                    return Headers


        # Проверка всех прокси, привязанных к аккаунтам
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка проксей каждой личности... Подождите немного!')
        for Account in Config:
            if Account['Proxy']:
                THREAD = Thread(target=HPV_Proxy_Check, args=(Account['Proxy'],))
                THREAD.start()
                THREADS.append(THREAD)


        for THREAD in THREADS:
            THREAD.join()


        # Определение свободных прокси
        FREE_PROXY = [PROXY for PROXY in ALL_PROXY if PROXY not in USE_PROXY]


        # Замена невалидных прокси
        for Account in Config:
            if Account['Proxy'] in INVALID_PROXY: # Если прокси уникальной личности невалиден
                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + f' — Найден невалидный прокси у `{Account["Name"]}`!')
                Account['Proxy'] = HPV_New_Proxy() # Новый прокси, взамен старого - нерабочего
                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + f' — Прокси у `{Account["Name"]}` успешно заменён!')
                CHANGES = True


        # Сравнение аккаунтов в `HPV_Account.json` и `HPV_Config.json`
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка наличия изменений в конфиге с аккаунтами... Подождите немного!')
        HPV_Account_Json, HPV_Config_Json = {(Name, URL) for Name, URL in Accounts.items()}, {(account['Name'], account['URL']) for account in Config}
        ACCOUNTS_TO_REMOVE = HPV_Config_Json - HPV_Account_Json # Неактуальные аккаунты
        NEW_ACCOUNTS = HPV_Account_Json - HPV_Config_Json # Новые аккаунты

        # Удаление неактуальных аккаунтов
        if ACCOUNTS_TO_REMOVE:
            print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Обнаружены неактуальные аккаунты. Производится их удаление...')
            NEW_CONFIG = [Account for Account in Config if (Account['Name'], Account['URL']) not in ACCOUNTS_TO_REMOVE] # Удаление неактуальных аккаунтов
            CHANGES = True

        # Добавление новых аккаунтов
        if NEW_ACCOUNTS:
            if not ACCOUNTS_TO_REMOVE:
                NEW_CONFIG = [Account for Account in Config] # Добавление текущих актуальных аккаунтов
            print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Обнаружены новые аккаунты. Выполняется их добавление...')
            for Name, URL in NEW_ACCOUNTS:
                Headers = HPV_New_Headers() # Генерация новых уникальных параметров для Headers
                NEW_CONFIG.append({'Name': Name, 'URL': URL, 'Proxy': HPV_New_Proxy(), 'Headers': Headers})
                USE_HEADERS.append(Headers)
                CHANGES = True


        # Сохранение данных при наличии изменений
        if CHANGES:
            print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Сохранение конфигурационных данных!')
            PATH = path.join(getcwd(), 'Core', 'Config', 'HPV_Config.json')
            with open(PATH, 'w', encoding='utf-8') as HPV:
                dump(NEW_CONFIG, HPV, ensure_ascii=False, indent=4)

    else:
        print(Fore.MAGENTA + '[HPV]' + Fore.YELLOW + ' — Конфигурационный файл не настроен или поврежден!')
        HPV_Config_Setup() # Настройка конфига








class HPV_Encrypt:
    '''Шифровальщик'''



    def __init__(self, Config: dict, Time: int) -> None:
        self.Start_Time = int(time() * 1000) # Время при старте игры
        self.End_Time = self.Start_Time + Time # Время при окончании игры
        self.Current_Time = self.Start_Time # Текущее время (во время процесса игры)

        self.Settings = Config['data']['cryptoMinerConfig']['itemSettingList'] # Настройки монет и мин
        self.Key = Config['data']['gameTag'].encode('utf-8') # Ключ для шифрования

        self.Game_Reward = 0 # Баланс игры
        self.Actions = [] # Список совершённых действий во время игры

        # Списки хранящие общее кол-во наград, мин и бонусов
        self.Game_Rewards = {Setting['size']: {'Total': Setting['quantity'], 'Reward': Setting['rewardValueList'][0]} for Setting in self.Settings if Setting['type'] == 'REWARD'}
        self.Game_Mines = {Setting['size']: {'Total': Setting['quantity'], 'Reward': Setting['rewardValueList'][0]} for Setting in self.Settings if Setting['type'] == 'TRAP'}
        self.Game_Bonus = {Setting['size']: {'Total': Setting['quantity'], 'Reward': Setting['rewardValueList'][0]} for Setting in self.Settings if Setting['type'] == 'BONUS'}



    def Encrypt(self) -> dict:
        '''Словарь с наградой и зашифрованной информацией об игре'''

        Payload = ';'.join(self.Actions).encode('utf-8')
        IV_Base64 = b64encode(GRB(12)).decode('utf-8')
        Encrypt_Base64 = b64encode(NEW(self.Key, CBC, IV_Base64[:16].encode('utf-8')).encrypt(Payload + (16 - len(Payload) % 16) * chr(16 - len(Payload) % 16).encode('utf-8'))).decode('utf-8')

        return {'Log': self.Game_Reward, 'Payload': IV_Base64 + Encrypt_Base64}



    def Generate_Actions(self) -> None:
        '''Генерация действий в игре'''

        while self.Current_Time < self.End_Time:

            self.Current_Time += randint(3500, 7500) # Совершение действия якобы каждые 3.5 - 7.5 секунд
            if self.Current_Time >= self.End_Time:
                break

            Random = random() # Генерация рандомного предмета

            # Выпавший предмет
            HPV = {'List': self.Game_Rewards, 'Type': 1} if Random < 0.65 else {'List': self.Game_Mines, 'Type': 1} if Random < 0.8 else {'List': self.Game_Bonus, 'Type': 2}

            # Проверка наличия предмета
            if HPV['List']:
                Size = choice(list(HPV['List'].keys())) # Размер предмета
                Type = HPV['Type'] # Тип предмета
                Reward = HPV['List'][Size]['Reward'] # Награда за предмет

                self.Game_Reward = max(0, self.Game_Reward + Reward) # Суммирование с общей наградой
                HPV['List'][Size]['Total'] -= 1 # Уменьшение кол-ва предметов, для избавления от повторов

                if HPV['List'][Size]['Total'] == 0: # Проверка наличия предмета
                    del HPV['List'][Size] # Удаление предмета при его отсутствии
            else:
                continue

            # Генерация положений и захвата предметов
            X1, Y1, Z, X2, Y2 = round(uniform(75, 275), 3), round(uniform(199, 251), 3), round(uniform(-1, 1), 3), round(uniform(100, 400), 3), round(uniform(250, 700), 3)
            self.Actions.append(f'{self.Current_Time}|{X1}|{Y1}|{Z}|{X2}|{Y2}|{Type}|{Size}|{Reward}')



    def Run(self) -> dict:
        '''Запуск'''

        try:
            self.Generate_Actions() # Генерация действий в игре
            return self.Encrypt() # Словарь с наградой и зашифрованной информацией об игре
        except:
            return {'Log': 0, 'Payload': ''}

def _HPV_Encrypt(Config: dict, Time: int) -> dict:
    '''Запуск шифровальщика'''

    Encrypt = HPV_Encrypt(Config, Time)
    return Encrypt.Run()



















class HPV_Moonbix:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Выполнение заданий`
    
    [2] - `Получение кол-ва доступных игр и запуск их прохождения`
    
    [3] - `Получение ежедневной награды`
    
    [4] - `Ожидание от 7 до 10 часов`
    
    [5] - `Повторение действий через 7-10 часа`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict, Headers: dict, AUTO_UPDATE: bool, Lock: Lock) -> None:
        self.HPV_PRO = Session()          # Requests сессия
        self.Name = Name                  # Ник аккаунта
        self.Proxy = Proxy                # Прокси (при наличии)
        self.URL = self.URL_Clean(URL)    # Уникальная ссылка для авторизации в mini app

        # Уникальные параметров для Headers
        self.UUID = Headers['UUID']
        self.WINDOWS = Headers['WINDOWS']
        self.USER_AGENT = Headers['USER_AGENT']
        self.SEC_CH_UA = Headers['SEC_CH_UA']
        self.SCREEN = Headers['SCREEN']
        self.BRAND_MODEL = Headers['BRAND_MODEL']
        self.SYSTEM_LANGUAGE = Headers['SYSTEM_LANGUAGE']
        self.Language = Headers['LANGUAGE']
        self.TIME_ZONE = Headers['TIME_ZONE']
        self.TIME_ZONE_OFFSET = Headers['TIME_ZONE_OFFSET']
        self.TIME_ZONE_WEB = Headers['TIME_ZONE_WEB']
        self.CANVAS_CODE = Headers['CANVAS_CODE']
        self.WEBGL_VENDOR = Headers['WEBGL_VENDOR']
        self.WEBGL_RENDERER = Headers['WEBGL_RENDERER']
        self.AUDIO = Headers['AUDIO']
        self.FINGERPRINT = Headers['FINGERPRINT']
        self.DEVICE_INFO = Headers['DEVICE_INFO']
        self.ACCEPT_LANGUAGE = self.Get_Accept_Language()

        self.AUTO_UPDATE = AUTO_UPDATE # Автоматическое обновление программы
        self.Console_Lock = Lock

        self.Token = self.Authentication()   # Токен аккаунта



    def URL_Clean(self, URL: str) -> str:
        '''Очистка уникальной ссылки от лишних элементов'''

        try:
            return unquote(URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except:
            return ''



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Smile: str, Text: str) -> None:
        '''Логирование'''

        with self.Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()        # Текущее время
            Name = Fore.MAGENTA + self.Name   # Ник аккаунта
            Smile = COLOR + str(Smile)        # Смайлик
            Text = COLOR + Text               # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Get_Accept_Language(self) -> str:
        '''Получение языкового параметра, подходящего под IP'''

        Accept_Language = HPV_Get_Accept_Language() # Получение данных с языковыми заголовками

        # Определение кода страны по IP
        try:
            COUNTRY = self.HPV_PRO.get('https://ipwho.is/', proxies=self.Proxy).json()['country_code'].upper()
        except:
            COUNTRY = ''

        return Accept_Language.get(COUNTRY, 'en-US,en;q=0.9')



    def Authentication(self) -> str:
        '''Аутентификация аккаунта'''

        UUID = str(uuid4())
        URL = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/third-party/access/accessToken'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'sec-ch-ua-platform': '"Windows"', 'x-trace-id': UUID, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'queryString': self.URL, 'socialType': 'telegram'}

        for _ in range(1, 72):
            self.Empty_Request(f'Authentication_{_}') # Пустой запрос

        try:
            Token = self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['data']['accessToken']
            self.Logging('Success', '🟢', 'Инициализация успешна!')
            return Token
        except:
            self.Logging('Error', '🔴', 'Ошибка инициализации!')
            return ''



    def ReAuthentication(self) -> None:
        '''Повторная аутентификация аккаунта'''

        self.Token = self.Authentication()



    def Empty_Request(self, Empty: str) -> None:
        '''Отправка пустых запросов с подгрузкой дополнений сайта, чтобы казаться человеком'''

        Request: dict = HPV_Get_Empty_Request()[Empty]

        for header_key in list(Request['Headers'].keys()):
            header_key_lower = header_key.lower()

            if header_key_lower == 'user-agent':
                Request['Headers'][header_key] = self.USER_AGENT
            elif header_key_lower == 'sec-ch-ua':
                Request['Headers'][header_key] = self.SEC_CH_UA
            elif header_key_lower == 'accept-language':
                Request['Headers'][header_key] = self.ACCEPT_LANGUAGE

        try:
            self.HPV_PRO.request(method=Request['Method'], url=Request['Url'], params=Request.get('Params'), data=Request.get('Data'), json=Request.get('Json'), headers=Request.get('Headers'), proxies=self.Proxy)
        except:
            pass



    def Get_Info(self) -> dict:
        '''Получение информации о балансе и играх'''

        UUID = str(uuid4())
        URL = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/user/user-info'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'x-growth-token': self.Token, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'fvideo-token': ''.join(choice(A + D + '+/') for _ in range(193)) + '=' + choice(D) + choice(A + D), 'sec-ch-ua-platform': '"Windows"', 'fvideo-id': token_hex(20), 'x-trace-id': UUID, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'resourceId': 2056}

        try:
            HPV = self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['data']['metaInfo']

            Balance = HPV['totalGrade'] + (HPV['referralTotalGrade'] if HPV['referralTotalGrade'] else 0) # Баланс
            Games = HPV['totalAttempts'] - HPV['consumedAttempts'] # Кол-во доступных игр

            return {'Balance': f'{Balance:,}', 'Games': Games}
        except:
            return {'Balance': '0', 'Games': 0}



    def Get_Tasks(self) -> list:
        '''Получение списка заданий'''

        UUID = str(uuid4())
        URL = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/task/list'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'x-growth-token': self.Token, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'fvideo-token': ''.join(choice(A + D + '+/') for _ in range(193)) + '=' + choice(D) + choice(A + D), 'sec-ch-ua-platform': '"Windows"', 'fvideo-id': token_hex(20), 'x-trace-id': UUID, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'resourceId': 2056}

        try:
            HPV = self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['data']['data'][0]['taskList']['data']

            TASKS = []

            for Task in HPV:
                if Task['status'] == 'IN_PROGRESS':
                    TASKS.append({'ID': Task['resourceId'], 'Reward': Task['rewardList'][0]['amount'], 'Type': Task['type']})

            return TASKS
        except:
            return []



    def Daily_Reward(self) -> bool:
        '''Ежедневная награда'''

        UUID = str(uuid4())
        URL = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/task/complete'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'x-growth-token': self.Token, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'fvideo-token': ''.join(choice(A + D + '+/') for _ in range(193)) + '=' + choice(D) + choice(A + D), 'sec-ch-ua-platform': '"Windows"', 'fvideo-id': token_hex(20), 'x-trace-id': UUID, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'resourceIdList': [2057], 'referralCode': None}

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['data']['status']
            return True
        except:
            return False



    def AutoDailyReward(self) -> None:
        '''Автоматическое получение ежедневной награды'''

        try:
            Tasks = self.Get_Tasks() # Получение списка заданий

            for Task in Tasks:
                if Task['Type'] == 'LOGIN':
                    if self.Daily_Reward():
                        self.Logging('Success', '🟢', f'Ежедневная награда получена! +{Task["Reward"]}')
                        sleep(randint(3, 5)) # Промежуточное ожидание
        except:
            pass



    def Start_Tasks(self, TaskID: int) -> bool:
        '''Выполнение задания'''

        UUID = str(uuid4())
        URL = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/task/complete'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'x-growth-token': self.Token, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'fvideo-token': ''.join(choice(A + D + '+/') for _ in range(193)) + '=' + choice(D) + choice(A + D), 'sec-ch-ua-platform': '"Windows"', 'fvideo-id': token_hex(20), 'x-trace-id': UUID, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'resourceIdList': [TaskID], 'referralCode': None}

        try:
            HPV = (self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['data']['status'] == 'COMPLETED')
            return True if HPV else False
        except:
            return False



    def AutoTasks(self) -> None:
        '''Автоматическое выполнение заданий'''

        try:
            Tasks = self.Get_Tasks() # Получение списка заданий

            for Task in Tasks:
                if self.Start_Tasks(Task['ID']):
                    self.Logging('Success', '⚡️', f'Задание выполнено! +{Task["Reward"]}')
                    self.Get_Info() # Пустой запрос
                    self.Get_Tasks() # Пустой запрос
                sleep(randint(5, 8)) # Промежуточное ожидание
        except:
            pass



    def Play(self) -> bool:
        '''Отыгрыш игры'''

        UUID_START = str(uuid4())
        URL_START = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/start'
        HEADERS_START = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'x-growth-token': self.Token, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'fvideo-token': ''.join(choice(A + D + '+/') for _ in range(193)) + '=' + choice(D) + choice(A + D), 'sec-ch-ua-platform': '"Windows"', 'fvideo-id': token_hex(20), 'x-trace-id': UUID_START, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID_START, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON_START = {'resourceId': 2056}

        self.Empty_Request('AutoGame_1') # Пустой запрос

        try:
            HPV = self.HPV_PRO.post(URL_START, headers=HEADERS_START, json=JSON_START, proxies=self.Proxy).json()
            self.Get_Info() # Пустой запрос

            Time = randint(47, 50) # Время ожидания игры
            self.Logging('Success', '🟢', f'Игра началась, ожидание {Time} секунд...')
            Actions = _HPV_Encrypt(HPV, Time * 1_000) # Запуск шифровальщика

            for _ in range(2, 18):
                self.Empty_Request(f'AutoGame_{_}') # Пустой запрос

            sleep(Time) # Ожидание конца игры

            UUID_END = str(uuid4())
            URL_END = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/complete'
            HEADERS_END = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'x-growth-token': self.Token, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'fvideo-token': ''.join(choice(A + D + '+/') for _ in range(193)) + '=' + choice(D) + choice(A + D), 'sec-ch-ua-platform': '"Windows"', 'fvideo-id': token_hex(20), 'x-trace-id': UUID_END, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID_END, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
            JSON_END = {'resourceId': 2056, 'payload': Actions['Payload'], 'log': Actions['Log']}

            HPV = self.HPV_PRO.post(URL_END, headers=HEADERS_END, json=JSON_END, proxies=self.Proxy).json()['success']
            if HPV:
                self.Logging('Success', '🟢', f'Игра сыграна! +{Actions["Log"]}!')
                self.Empty_Request('AutoGame_18') # Пустой запрос
                self.Empty_Request('AutoGame_19') # Пустой запрос
                self.Get_Info() # Пустой запрос
                return True
            else:
                self.Logging('Error', '🔴', 'Игра не сыграна!')
                return False
        except:
            self.Logging('Error', '🔴', 'Игра не сыграна!')
            return False



    def AutoGame(self, Games: int) -> None:
        '''Автоматический отыгрыш игр'''

        try:
            if Games > 0:
                self.Logging('Success', '🎮', f'Игр доступно: {Games}!')

                for _ in range(Games):
                    self.Play() # Отыгрыш игры
                    sleep(randint(4, 6)) # Промежуточное ожидание
        except:
            pass



    def AutoCheckLeaderBoard(self) -> None:
        '''Автоматический просмотр лидер борда'''

        UUID = str(uuid4())
        URL = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/summary/list'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'x-growth-token': self.Token, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'fvideo-token': ''.join(choice(A + D + '+/') for _ in range(193)) + '=' + choice(D) + choice(A + D), 'sec-ch-ua-platform': '"Windows"', 'fvideo-id': token_hex(20), 'x-trace-id': UUID, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'resourceId': 2056, 'pageSize': 100}

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy)
        except:
            pass



    def AutoCheckReferrals(self) -> None:
        '''Автоматический просмотр списка рефералов'''

        UUID = str(uuid4())
        URL = 'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/referral/list'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'lang': self.Language, 'x-growth-token': self.Token, 'device-info': self.DEVICE_INFO, 'bnc-uuid': self.UUID, 'fvideo-token': ''.join(choice(A + D + '+/') for _ in range(193)) + '=' + choice(D) + choice(A + D), 'sec-ch-ua-platform': '"Windows"', 'fvideo-id': token_hex(20), 'x-trace-id': UUID, 'sec-ch-ua-mobile': '?0', 'x-ui-request-trace': UUID, 'clienttype': 'web', 'origin': 'https://www.binance.com', 'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://www.binance.com/ru/game/tg/moon-bix', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'resourceId': 2056, 'pageIndex': 1, 'pageSize': 300}

        self.Empty_Request('AutoCheckReferrals') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy)
        except:
            pass



    def AutoCheckVerif(self) -> None:
        '''Автоматический просмотр страницы верификации аккаунта Binance'''

        self.Empty_Request('AutoCheckVerif') # Пустой запрос



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Token: # Если аутентификация успешна

                    INFO = self.Get_Info()
                    Balance = INFO['Balance'] # Баланс
                    Games = INFO['Games'] # Кол-во доступных игр
                    self.Logging('Success', '💰', f'Баланс: {Balance}')


                    # Автоматическое получение ежедневной награды
                    self.AutoDailyReward()


                    # Проверка на недавний сбор
                    if Games < 2:
                        _Waiting = randint(7*60*60, 10*60*60) # Значение времени в секундах для ожидания
                        _Waiting_STR = (datetime.now() + timedelta(seconds=_Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                        self.Logging('Warning', '⏳', f'Сбор уже производился! Следующий сбор: {_Waiting_STR}!')

                        # Ожидание от 7 до 10 часов
                        _Waiting_For_Upgrade = int(_Waiting / (60*30))
                        for _ in range(_Waiting_For_Upgrade):
                            if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                                return
                            sleep(60*30)
                        sleep(_Waiting - (_Waiting_For_Upgrade * 60 * 30))
                        self.ReAuthentication() # Повторная аутентификация аккаунта
                        continue


                    # Рандомное выполнение действий: 
                    Autos = [lambda: self.AutoGame(Games), self.AutoTasks, self.AutoCheckLeaderBoard, self.AutoCheckReferrals, self.AutoCheckVerif]
                    shuffle(Autos) # Перемешивание списока функций
                    for Auto in Autos:
                        Auto()
                        sleep(randint(3, 6)) # Промежуточное ожидание


                    Waiting = randint(7*60*60, 10*60*60) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде


                    self.Logging('Success', '💰', f'Баланс: {self.Get_Info()["Balance"]}')
                    self.Logging('Warning', '⏳', f'Следующий сбор: {Waiting_STR}!')


                    # Ожидание от 7 до 10 часов
                    Waiting_For_Upgrade = int(Waiting / (60*30))
                    for _ in range(Waiting_For_Upgrade):
                        if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                            return
                        sleep(60*30)
                    sleep(Waiting - (Waiting_For_Upgrade * 60 * 30))
                    self.ReAuthentication() # Повторная аутентификация аккаунта

                else: # Если аутентификация не успешна
                    if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                        return
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
                    self.ReAuthentication() # Повторная аутентификация аккаунта

            except:
                if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                    return
                sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд




















def HPV_Main(AUTO_UPDATE: bool) -> None:
    '''Запуск Moonbix'''

    if s_name() == 'Windows':
        sys(f'cls && title HPV Moonbix - V{VERSION}')
    else:
        sys('clear')

    while True:
        HPV_Banner() # Вывод баннера
        HPV_Config_Check(AUTO_UPDATE) # Проверка конфига на валидность
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка конфига окончена... Скрипт запустится через 5 секунд...\n'); sleep(5)

        Console_Lock = Lock()
        Threads = [] # Список потоков

        def Start_Thread(Name: str, URL: str, Proxy: dict, Headers: dict) -> None:
            Moonbix = HPV_Moonbix(Name, URL, Proxy, Headers, AUTO_UPDATE, Console_Lock)
            Moonbix.Run()

        # Получение конфигурационных данных и запуск потоков
        for Account in HPV_Get_Config(_print=False):
            HPV = Thread(target=Start_Thread, args=(Account['Name'], Account['URL'], Account['Proxy'], Account['Headers'],))
            HPV.start()
            Threads.append(HPV)

        for thread in Threads:
            thread.join()






