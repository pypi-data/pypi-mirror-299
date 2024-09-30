from requests import Session, get
from urllib.parse import unquote, quote
from colorama import Fore
from datetime import datetime, timedelta
from threading import Thread, Lock
from typing import Literal
from random import randint, shuffle, choice
from os import system as sys, getcwd, path
from platform import system as s_name
from time import sleep, time
from shutil import get_terminal_size as gts
from collections import Counter
from json import dump, dumps, load, loads
from subprocess import run as terminal, Popen
from sys import exit, executable
from hashlib import sha256
from hmac import new
from math import ceil


VERSION = '3.0.1'




















HPV_TEAM = f'''
 _  _ _____   __   ___ _   _ __  __ ___ 
| || | _ \ \ / /__| _ ) | | |  \/  | _ \\
| __ |  _/\ V /___| _ \ |_| | |\/| |  _/
|_||_|_|   \_/    |___/\___/|_|  |_|_|  
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
                "Url": "https://mmbump.pro/static/css/main.475864a4.css",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "text/css,*/*;q=0.1", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "style", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "Authentication_2": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/js/main.bc2cfbdd.js",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "script", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "Authentication_3": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/SF-Pro-Display-Regular.d1f5e6e16dd4f75c3950.otf",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://mmbump.pro", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://mmbump.pro/static/css/main.475864a4.css", "accept-language": "HPV TEAM"}
            },
            "Authentication_4": {
                "Method": "get",
                "Url": "https://mmbump.pro/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/announcement", "accept-language": "HPV TEAM"}
            },
            "Authentication_5": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/moon-top.ad691e6ad76abfb8ea0c.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/announcement", "accept-language": "HPV TEAM"}
            },
            "Authentication_6": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/IllustrationBottom.b911c7f95eb71168f0ce.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/announcement", "accept-language": "HPV TEAM"}
            },
            "Authentication_7": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/SF-Pro-Display-Semibold.037dc63930459813f575.otf",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://mmbump.pro", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://mmbump.pro/static/css/main.475864a4.css", "accept-language": "HPV TEAM"}
            },
            "Authentication_8": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/SF-Pro-Display-Bold.b1f4d2c69fa808ebca12.otf",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://mmbump.pro", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://mmbump.pro/static/css/main.475864a4.css", "accept-language": "HPV TEAM"}
            },
            "Authentication_9": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/SF-Pro-Display-Medium.b85d841dacb040b84951.otf",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://mmbump.pro", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://mmbump.pro/static/css/main.475864a4.css", "accept-language": "HPV TEAM"}
            },
            "Authentication_10": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/SF-Pro-Display-Light.5a47a04ca76b10e69ca3.otf",
                "Headers": {"User-Agent": "HPV TEAM", "sec-ch-ua": "HPV TEAM", "origin": "https://mmbump.pro", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "cors", "sec-fetch-dest": "font", "referer": "https://mmbump.pro/static/css/main.475864a4.css", "accept-language": "HPV TEAM"}
            },
            "Authentication_11": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/loginJwt",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "Authentication_12": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/leagueSlide.7b8039e90cf508a902b1.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/announcement", "accept-language": "HPV TEAM"}
            },
            "Authentication_13": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/announcement-11.bd84dd8227d33f9e07cd.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/announcement", "accept-language": "HPV TEAM"}
            },
            "Authentication_14": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/announcement-22.c60aa6a82aff7afbc82e.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/announcement", "accept-language": "HPV TEAM"}
            },
            "Authentication_15": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/announcement-23.ddee38c3b44a1ad28bb3.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/announcement", "accept-language": "HPV TEAM"}
            },
            "Authentication_16": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/CornerLeft.221f2df323e180bb4faa.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u", "accept-language": "HPV TEAM"}
            },
            "Authentication_17": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/CornerRight.60aabb6b5475824d6340.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u", "accept-language": "HPV TEAM"}
            },
            "Authentication_18": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/IllustrationBottomLayout.4bda8e59622ea00f1e4d.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u", "accept-language": "HPV TEAM"}
            },
            "Authentication_19": {
                "Method": "get",
                "Url": "https://mmbump.pro/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u", "accept-language": "HPV TEAM"}
            },



            "Get_Info": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/farming",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },



            "Farm_1": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/farming/start",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "Farm_2": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/farming/finish",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "Farm_3": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/farming/moon-claim",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },



            "NFTs_1": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/nft/market",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "NFTs_2": {
                "Method": "get",
                "Url": "https://mmbump.pro/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/nfts/marketplace", "accept-language": "HPV TEAM"}
            },
            "NFTs_3": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/nft/market/collections",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "NFTs_4": {
                "Method": "get",
                "Url": "https://mmbump.pro/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/nfts/my-nfts", "accept-language": "HPV TEAM"}
            },



            "AutoBuyBoost_1": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/CornerBoosters.c170db3a693c030e1677.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/boosters", "accept-language": "HPV TEAM"}
            },
            "AutoBuyBoost_2": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/booster-background-small.f4447fa5622af7be1d7b.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/boosters", "accept-language": "HPV TEAM"}
            },
            "AutoBuyBoost_3": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/x3.009d60a557d3500fc770.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/boosters", "accept-language": "HPV TEAM"}
            },
            "AutoBuyBoost_4": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/x2.eafdc7fc7f41d48fb6bb.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/boosters", "accept-language": "HPV TEAM"}
            },
            "AutoBuyBoost_5": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/booster-background-big.81f3ffc68bd673fdaddc.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/boosters", "accept-language": "HPV TEAM"}
            },
            "AutoBuyBoost_6": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/x5.3412c9c2912fd0328234.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/boosters", "accept-language": "HPV TEAM"}
            },
            "AutoBuyBoost_7": {
                "Method": "get",
                "Url": "https://mmbump.pro/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/boosters", "accept-language": "HPV TEAM"}
            },
            "AutoBuyBoost_8": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/product-list/buy",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },



            "AutoRefClaim_1": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/IllustrationTopLayout.ded4b832e17a62ed15b7.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/friends", "accept-language": "HPV TEAM"}
            },
            "AutoRefClaim_2": {
                "Method": "get",
                "Url": "https://mmbump.pro/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/friends", "accept-language": "HPV TEAM"}
            },
            "AutoRefClaim_3": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/friends",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "AutoRefClaim_4": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/friends/claim",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },



            "AutoTasks_1": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/IllustrationTopLayout.ded4b832e17a62ed15b7.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/kols", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_2": {
                "Method": "get",
                "Url": "https://mmbump.pro/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/kols", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_3": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/task-list",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_4": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/task-list/complete",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_5": {
                "Method": "options",
                "Url": "https://api.mmbump.pro/v1/grant-day/claim",
                "Headers": {"User-Agent": "HPV TEAM", "access-control-request-method": "POST", "access-control-request-headers": "authorization,content-type,user_auth", "origin": "https://mmbump.pro", "sec-fetch-mode": "cors", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-site", "sec-fetch-dest": "empty", "referer": "https://mmbump.pro/", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_6": {
                "Method": "get",
                "Url": "https://mmbump.pro/favicon.ico",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/community", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_7": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/noPrize.f72a62f95f1ba6897e0d.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/daily", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_8": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/daily-reward-1.b41f3ebe802989042c86.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/daily", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_9": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/daily-reward-7.0aa97390791490043892.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/daily", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_10": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/daily-reward-14.92cbb11a2405eef01c62.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/daily", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_11": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/daily-reward-21.339ebdd6c472b889190d.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/daily", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_12": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/daily-reward-28.8ee0f08abca2dfc5631b.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/daily", "accept-language": "HPV TEAM"}
            },
            "AutoTasks_13": {
                "Method": "get",
                "Url": "https://mmbump.pro/static/media/Ship-group.425edc68bb745602a732.png",
                "Headers": {"User-Agent": "HPV TEAM", "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "sec-ch-ua": "HPV TEAM", "sec-ch-ua-mobile": "HPV TEAM", "sec-ch-ua-platform": "HPV TEAM", "x-requested-with": "HPV TEAM", "sec-fetch-site": "same-origin", "sec-fetch-mode": "no-cors", "sec-fetch-dest": "image", "referer": "https://mmbump.pro/u/tasks/daily", "accept-language": "HPV TEAM"}
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









def HPV_Headers() -> dict:
    '''Генератор уникальных параметров для Headers'''

    HPV_CHROME_VERSION = [

        '126.0.6478.111', # 25/06/2024
        '126.0.6478.110', # 19/06/2024
        '126.0.6478.72',  # 19/06/2024
        '126.0.6478.71',  # 14/06/2024
        '125.0.6422.186', # 14/06/2024
        '126.0.6478.50',  # 12/06/2024
        '125.0.6422.167', # 12/06/2024
        '125.0.6422.165', # 05/06/2024
        '125.0.6422.164', # 05/06/2024
        '125.0.6422.113', # 24/05/2025
        '125.0.6422.112', # 24/05/2025
        '125.0.6422.72',  # 22/05/2024
        '125.0.6422.71',  # 22/05/2024
        '125.0.6422.53',  # 16/05/2024
        '125.0.6422.52',  # 16/05/2024
        '124.0.6367.82',  # 24/04/2024
        '123.0.6312.121', # 24/04/2024
        '124.0.6367.54',  # 16/04/2024
        '123.0.6312.120', # 16/04/2024
        '123.0.6312.119', # 16/04/2024
        '123.0.6312.99',  # 03/04/2024
        '123.0.6312.81',  # 03/04/2024
        '123.0.6312.80',  # 27/03/2024
        '123.0.6312.41',  # 27/03/2024
        '123.0.6312.40',  # 20/03/2024
        '122.0.6261.120', # 20/03/2024
        '122.0.6261.119', # 13/03/2024
        '122.0.6261.106', # 13/03/2024

    ]
    HPV_PHONE_MODEL = [

        'Xiaomi Redmi K60 Pro',
        'Realme C33',
        'Realme Pad 2',
        'Realme Note 50',
        'Realme GT Neo 3T',
        'Xiaomi Redmi Pad Pro',
        'Realme Q5 Pro',
        'Realme 10 Pro',
        'Xiaomi Pad 6 Max 14',
        'Infinix Hot 11s',
        'Xiaomi Redmi A3',
        'Xiaomi Redmi Turbo 3',
        'Xiaomi Redmi Pad SE',
        'Infinix Hot 40 Pro',
        'Realme C65',
        'Xiaomi Redmi Note 11T Pro',
        'Xiaomi 12T',
        'Realme 12 Pro+',
        'Infinix Hot 12',
        'Realme Q5i',
        'Realme V25',
        'Xiaomi Redmi K70 Ultra',
        'Xiaomi 14 Pro',
        'Xiaomi Redmi 12',
        'Xiaomi Redmi Note 12 Turbo',
        'Infinix Smart 7',
        'Infinix Smart 8 Plus',
        'Xiaomi Mix Fold 4',
        'Xiaomi Civi 4 Pro',
        'Xiaomi Redmi Note 11 Pro',
        'Xiaomi Redmi Note 12S',
        'Realme C53',
        'Xiaomi Redmi Note 13 Pro',
        'Realme GT 6T',
        'Realme C67',
        'Xiaomi Poco F6 Pro',
        'Xiaomi Mix Flip',
        'Xiaomi Redmi K70 Pro',
        'Xiaomi 11i HyperCharge',
        'Infinix Hot 30i',
        'Realme 12 Lite',
        'Realme 9i',
        'Infinix Smart 8',
        'Realme 10',
        'Xiaomi Civi 1S',
        'Infinix Note 30',
        'Realme 13 Pro+',
        'Xiaomi Redmi 10A',
        'Xiaomi Poco M5s',
        'Realme GT5 Pro',
        'Infinix Zero',
        'Xiaomi 12S Pro',
        'Xiaomi Redmi Note 12',
        'Realme Narzo 50A Prime',
        'Xiaomi Redmi 12C',
        'Infinix Note 12i',
        'Xiaomi 13 Lite',
        'Xiaomi Poco M6 Plus',
        'Samsung Galaxy S22 Ultra',
        'Xiaomi 14 Civi',
        'Xiaomi Redmi A2',
        'Xiaomi Poco M4',
        'Xiaomi Poco M4 Pro',
        'Xiaomi Redmi 11 Prime',
        'Infinix Note 40',
        'Xiaomi Redmi 10 Power',
        'Xiaomi Poco C55',
        'Infinix Zero 30',
        'Xiaomi Redmi K40S',
        'Xiaomi Poco C65',
        'Xiaomi Redmi Note 11E',
        'Xiaomi Poco M6 Pro',
        'Xiaomi Pad 6S Pro 12.4',
        'Xiaomi Poco X4 GT',
        'Realme GT Neo 3',
        'Realme 11 Pro',
        'Realme 10s',
        'Infinix Note 40 Pro',
        'Realme C63',
        'Xiaomi Redmi Note 12 Pro',
        'Infinix Hot 30 Play',
        'Realme Narzo 50i Prime',
        'Xiaomi 12S Ultra',
        'Infinix Hot 40i',
        'Realme C30s',
        'Realme Pad Mini',
        'Infinix Smart 8 Pro',
        'Xiaomi Redmi 10 2022',
        'Xiaomi Redmi K60E',
        'Xiaomi 13T Pro',
        'Xiaomi Mix Fold 2',
        'Realme C35',
        'Infinix Note 12 Pro',
        'Xiaomi 12 Lite',
        'Infinix Hot 12 Play',
        'Xiaomi Poco C50',
        'Xiaomi 11i',
        'Realme Narzo 50',
        'Xiaomi 13T',
        'Xiaomi Redmi K50 Pro',
        'Realme 9 Pro',
        'Xiaomi 13 Ultra',
        'Xiaomi Poco M5',
        'Xiaomi Poco F4 GT',
        'Xiaomi Poco F5',
        'Xiaomi Poco F5 Pro',
        'Xiaomi Redmi Note 12T Pro',
        'Xiaomi Redmi Note 11E Pro',
        'Realme V23',
        'Xiaomi Pad 6',
        'Xiaomi Redmi Note 12 Pro Speed',
        'Realme C51s',
        'Realme GT5 240W',
        'Xiaomi Poco F6',
        'Xiaomi Redmi K70E',
        'Realme C30',
        'Xiaomi Redmi A3x',
        'Realme C61',
        'Xiaomi Mix Fold 3',
        'Realme C51',
        'Xiaomi Redmi K60 Ultra',
        'Xiaomi Redmi 10C',
        'Xiaomi Redmi A1',
        'Realme C31',
        'Infinix Note 12',
        'Realme V30',
        'Realme C55',
        'Xiaomi 14 Ultra',
        'Realme GT 6',
        'Xiaomi Poco C61',
        'Xiaomi Redmi K50i',
        'Infinix Hot 12 Pro',
        'Xiaomi Redmi Note 11',
        'Realme Narzo N53',
        'Infinix Smart 7 HD',
        'Xiaomi Redmi Note 11S',
        'Xiaomi Poco X4',
        'Xiaomi Poco X4 Pro',
        'Realme Pad X',
        'Xiaomi Redmi Note 13R',
        'Infinix Smart 8 HD',
        'Xiaomi Poco C51',
        'Infinix Hot 20',
        'Xiaomi Civi 3',
        'Xiaomi Poco F4',
        'Realme V23i',
        'Xiaomi 12T Pro',
        'Xiaomi Redmi 13C',
        'Honor X8B',
        'Honor Magic6 Pro',
        'Honor Magic6 Ultimate',
        'Honor X9b',
        'Honor 200 Lite',
        'Huawei Pura 70 Ultra',
        'Huawei Pura 70 Pro',
        'Huawei Pura 70',
        'Huawei nova 12s',
        'Huawei nova Y72',
        'Xiaomi Redmi Note 10T',
        'Xiaomi POCO X6',
        'Xiaomi POCO X6 Pro',
        'Xiaomi POCO M6 Pro',
        'Xiaomi POCO X5',
        'Xiaomi POCO X5 Pro',
        'Xiaomi POCO C40',
        'Xiaomi POCO M5s',
        'Xiaomi POCO M5',
        'Samsung Galaxy A05',
        'Samsung Galaxy A35',
        'Samsung Galaxy S24',
        'Samsung Galaxy S24+',
        'Samsung Galaxy S24 Ultra',
        'Samsung Galaxy A15',
        'Samsung Galaxy A25',
        'Samsung Z Flip5',
        'Samsung Galaxy A05s',
        'Samsung Galaxy A24',
        'Samsung Galaxy A14',
        'Samsung Galaxy S23 FE',
        'Samsung Galaxy Z Fold5',
        'Samsung Galaxy A34',
        'Samsung Galaxy M54',
        'Samsung Galaxy A54',
        'Samsung Galaxy S23+',
        'Samsung Galaxy S23',
        'Samsung Galaxy S23 Ultra',
        'Samsung Galaxy A03',
        'Samsung Galaxy A04',
        'Samsung Galaxy XCover6 Pro',
        'Samsung Galaxy A13',
        'Samsung Galaxy A23',
        'Samsung Galaxy M23',
        'Samsung Galaxy A33',
        'Samsung Galaxy A73',
        'Samsung Galaxy A53',
        'Samsung Galaxy Z Fold4',
        'Samsung Galaxy S22',
        'Samsung Galaxy S22+',
        'Samsung S21 FE',
        'vivo X100 Ultra',
        'vivo V30e',
        'vivo V30 lite',
        'vivo X100',
        'vivo Y27s',
        'vivo X100 Pro',
        'vivo V29e',
        'vivo V29',
        'vivo Y36',
        'vivo V27',
        'vivo V27e',
        'vivo X Note',
        'vivo X80 Pro',
        'vivo T1',
        'vivo X90 Pro',
        'vivo X90 Pro+',
        'vivo V25 Pro',
        'vivo Y35',
        'vivo V25',
        'vivo v23e',
        'vivo v23',
        'OPPO Reno11',
        'OPPO Find X7 Ultra',
        'OPPO Find X7',
        'OPPO Find N2'

    ]
    HPV_TELEGRAM_CLIENT = [

        'org.telegram.messenger', # Telegram
        'org.telegram.plus',      # Plus
        'ir.ilmili.telegraph',    # Telegraph

    ]

    HPV_Chrome_Version = choice(HPV_CHROME_VERSION) # Версия Google Chrome
    HPV_Android_Version = randint(11, 14) # Версия Android
    HPV_Phone_Model = choice(HPV_PHONE_MODEL) # Модель телефона
    HPV_Telegram_Client = choice(HPV_TELEGRAM_CLIENT) # Клиент Telegram

    USER_AGENT = f'Mozilla/5.0 (Linux; Android {HPV_Android_Version}; {HPV_Phone_Model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{HPV_Chrome_Version} Mobile Safari/537.36'
    SEC_CH_UA = f'"Chromium";v="{HPV_Chrome_Version.split(".")[0]}", "Not(A:Brand";v="99", "Google Chrome";v="{HPV_Chrome_Version.split(".")[0]}"'
    SEC_CH_UA_MOBILE = '?1'
    SEC_CH_UA_PLATFORM = '"Android"'
    X_REQUESTED_WITH = HPV_Telegram_Client

    return {'USER_AGENT': USER_AGENT, 'SEC_CH_UA': SEC_CH_UA, 'SEC_CH_UA_MOBILE': SEC_CH_UA_MOBILE, 'SEC_CH_UA_PLATFORM': SEC_CH_UA_PLATFORM, 'X_REQUESTED_WITH': X_REQUESTED_WITH}




















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
            HPV = get('https://pypi.org/pypi/HPV-TEAM-BUMP/json').json()['info']['version']
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
                terminal([PIP, 'install', '--upgrade', 'HPV_TEAM_BUMP'], check=True) # Установка зависимостей

                print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Перезапуск программы...')
                Popen([executable, path.join(getcwd(), 'HPV_BUMP.py')]); exit() # Перезапуск программы

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
        HPV_Account_json: {'ACCOUNT_1': 'https://mmbump.pro/#tgWebAppData=....', 'ACCOUNT_2': 'https://mmbump.pro/#tgWebAppData=....'},
        HPV_Config_json: '',
        HPV_Config_py: '\n\n# Желаемое кол-во получаемых монет за период фарма. Рандомным путём будет выбрано значение в следующих диапазонах\nCOINS = [37951, 81159] # 37,951 - минимальное значение /// 81,159 - максимальное\n# Ставить максимальное значение выше 100К не рекомендуется!\n\n\n# Автоматическая покупка буста X5 для ускоренного фарма\nBUY_BOOST = True # Для включения установите значение True, для отключения — False.\n# По умолчанию значение включено, однако, вы можете его отключить\n\n\n# Автоматическое обновление программы\nAUTO_UPDATE = False # Для включения установите значение True, для отключения — False.\n# По умолчанию автообновление включено, и рекомендуется не изменять этот параметр. Однако, вы можете его отключить по соображениям безопасности!\n\n',
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




















class HPV_BUMP:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Получение ежедневной награды`
    
    [2] - `Выполнение заданий
    
    [3] - `Сбор монет и запуск фарма`
    
    [4] - `Сбор монет за рефералов`
    
    [5] - `Покупка буста`
    
    [6] - `Ожидание от 10 до 13 часов`
    
    [7] - `Повторение действий через 10-13 часов`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict, Headers: dict, COINS: list[int], BUY_BOOST: bool, AUTO_UPDATE: bool, Lock: Lock) -> None:
        self.HPV_PRO = Session()       # Создание `requests` сессии
        self.Name = Name               # Ник аккаунта
        self.Proxy = Proxy             # Прокси (при наличии)

        INFO = self.URL_Clean(URL)
        self.TG_ID = INFO['ID']        # ID аккаунта
        self.URL = INFO['URL']         # Уникальная ссылка для авторизации в mini app
        self.Domain = INFO['Domain']   # Домен игры

        # Уникальные параметров для Headers
        self.USER_AGENT = Headers['USER_AGENT']
        self.SEC_CH_UA = Headers['SEC_CH_UA']
        self.SEC_CH_UA_MOBILE = Headers['SEC_CH_UA_MOBILE']
        self.SEC_CH_UA_PLATFORM = Headers['SEC_CH_UA_PLATFORM']
        self.X_REQUESTED_WITH = Headers['X_REQUESTED_WITH']
        self.ACCEPT_LANGUAGE = self.Get_Accept_Language()

        # Конфиг
        self.COINS = COINS # Желаемое кол-во получаемых монет за одну игру
        self.BUY_BOOST = BUY_BOOST # Автоматическая покупка буста X5
        self.AUTO_UPDATE = AUTO_UPDATE # Автоматическое обновление программы

        self.Console_Lock = Lock

        self.Token = self.Authentication()   # Токен аккаунта



    def URL_Clean(self, URL: str) -> dict:
        '''Очистка уникальной ссылки от лишних элементов'''

        try:
            ID = str(loads(unquote(unquote(unquote(URL.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))).split('&')[1].split('user=')[1])['id'])
        except:
            ID = ''

        try:
            _URL = unquote(URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except:
            _URL = ''

        return {'ID': ID, 'URL': _URL, 'Domain': 'https://api.mmbump.pro/v1/'}



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

        URL = self.Domain + 'loginJwt'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vYXBpLm1tYnVtcC5wcm8vdjEvbG9naW5Kd3QiLCJpYXQiOjE3MjYxNTQwNTEsImV4cCI6MTcyNjE1NzY1MSwibmJmIjoxNzI2MTU0MDUxLCJqdGkiOiJwYWR4d3VtOFRzcTIxeEx1Iiwic3ViIjoiNDc4MDgzIiwicHJ2IjoiMTUzNTk0YmFlZWRkY2Q5OTQ3ODJhNjkwNWZiZmQ1NjA0MmM5ZThjOSIsImNoYXRfaWQiOjEyOTUzMjA5Njd9.qUnDlksQblFiYvSKNEbPOx2oOqMFh0V5gZx9YSeQ7zQ', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'initData': self.URL}

        self.Empty_Request('Authentication_1') # Пустой запрос
        self.Empty_Request('Authentication_2') # Пустой запрос
        self.Empty_Request('Authentication_3') # Пустой запрос
        self.Empty_Request('Authentication_4') # Пустой запрос
        self.Empty_Request('Authentication_5') # Пустой запрос
        self.Empty_Request('Authentication_6') # Пустой запрос
        self.Empty_Request('Authentication_7') # Пустой запрос
        self.Empty_Request('Authentication_8') # Пустой запрос
        self.Empty_Request('Authentication_9') # Пустой запрос
        self.Empty_Request('Authentication_10') # Пустой запрос
        self.Empty_Request('Authentication_11') # Пустой запрос

        try:
            Token = self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['access_token']
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
            elif header_key_lower == 'sec-ch-ua-mobile':
                Request['Headers'][header_key] = self.SEC_CH_UA_MOBILE
            elif header_key_lower == 'sec-ch-ua-platform':
                Request['Headers'][header_key] = self.SEC_CH_UA_PLATFORM
            elif header_key_lower == 'x-requested-with':
                Request['Headers'][header_key] = self.X_REQUESTED_WITH
            elif header_key_lower == 'accept-language':
                Request['Headers'][header_key] = self.ACCEPT_LANGUAGE

        try:
            self.HPV_PRO.request(method=Request['Method'], url=Request['Url'], params=Request.get('Params'), data=Request.get('Data'), json=Request.get('Json'), headers=Request.get('Headers'), proxies=self.Proxy)
        except:
            pass



    def Hash_Gen(self, Params: list[dict]):
        '''Генерация хеша'''

        _Params = '&'.join([f"{KEY}={quote(str(VALUE))}" for Param in Params for KEY, VALUE in Param.items()])
        _Time = f'time={ceil(0 / 60)}'
        _Hash = f'{_Params}&{_Time}' if _Params else _Time
        Hash = new('JW1eBE3kS9bTC7gM2vhZIH5yG26hmZrc'.encode(), _Hash.encode(), sha256).hexdigest()

        return Hash



    def Get_Info(self) -> dict:
        '''Получение информации о юзере'''

        URL = self.Domain + 'farming'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'user_auth': self.TG_ID, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}

        self.Empty_Request('Get_Info') # Пустой запрос

        try:
            HPV = self.HPV_PRO.post(URL, headers=HEADERS, proxies=self.Proxy).json()

            Balance = HPV['balance'] # Баланс
            Boost = True if HPV['info'].get('active_booster_finish_at') else False # Наличие купленного буста
            Daily_Reward = HPV['day_grant_first'] + 24*60*60 if HPV['day_grant_first'] else False # Ежедневная награда
            Start_Farm = HPV['session'].get('start_at') if HPV['session'].get('start_at') else False # Начало фарма

            return {'Balance': f'{Balance:,}', 'Boost': Boost, 'Daily_Reward': Daily_Reward, 'Start_Farm': Start_Farm}
        except:
            return {'Balance': '0', 'Boost': False, 'Daily_Reward': False, 'Start_Farm': False}



    def Start_Farm(self) -> bool:
        '''Старт фарма'''

        URL = self.Domain + 'farming/start'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'status': 'inProgress', 'hash': self.Hash_Gen([{'status': 'inProgress'}])}

        self.Empty_Request('Farm_1') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['status']
            return True
        except:
            return False



    def Finish_Farm(self) -> bool:
        '''Завершение и сбор фарма'''

        _COINS = randint(self.COINS[0], self.COINS[1]) # Желаемое кол-во получения монет
        URL = self.Domain + 'farming/finish'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'tapCount': _COINS, 'hash': self.Hash_Gen([{'tapCount': _COINS}])}

        self.Empty_Request('Farm_2') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['session']['finish_at']
            return True
        except:
            return False



    def AutoFarm(self) -> None:
        '''Автоматический фарм'''

        try:
            # Завершение и сбор фарма
            if self.Finish_Farm():
                self.Logging('Success', '🟣', 'Сбор после фарминга произведён!')

            sleep(randint(3, 5)) # Промежуточное ожидание

            # Старт фарма
            if self.Start_Farm():
                self.Logging('Success', '🟣', 'Фарм запущен!')
        except:
            pass



    def Buy_Boost(self) -> bool:
        '''Покупка буста'''

        URL = self.Domain + 'product-list/buy'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'id': 'x5', 'hash': self.Hash_Gen([{'id': 'x5'}])}

        self.Empty_Request('AutoBuyBoost_8') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['id']
            return True
        except:
            return False



    def AutoBuyBoost(self, Boost: bool) -> None:
        '''Автоматическая покупка буста'''

        try:
            self.Empty_Request('AutoBuyBoost_1') # Пустой запрос
            self.Empty_Request('AutoBuyBoost_2') # Пустой запрос
            self.Empty_Request('AutoBuyBoost_3') # Пустой запрос
            self.Empty_Request('AutoBuyBoost_4') # Пустой запрос
            self.Empty_Request('AutoBuyBoost_5') # Пустой запрос
            self.Empty_Request('AutoBuyBoost_6') # Пустой запрос
            self.Empty_Request('AutoBuyBoost_7') # Пустой запрос

            sleep(randint(3, 5)) # Промежуточное ожидание

            if not Boost and self.BUY_BOOST:
                if self.Buy_Boost():
                    self.Logging('Success', '⭐️', 'Буст `X5` преобретён!')
                    self.Get_Info() # Пустой запрос
        except:
            pass



    def Referal_Claim(self) -> bool:
        '''Сбор монет за рефералов'''

        URL = self.Domain + 'friends/claim'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'hash': self.Hash_Gen([])}

        self.Empty_Request('AutoRefClaim_4') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['sum']
            return True
        except:
            return False



    def AutoRefClaim(self) -> None:
        '''Автоматический сбор монет за рефералов'''

        URL = self.Domain + 'friends'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'hash': self.Hash_Gen([{'offset': 0, 'limit': 20}]), 'offset': 0, 'limit': 20}

        self.Empty_Request('AutoRefClaim_1') # Пустой запрос
        self.Empty_Request('AutoRefClaim_2') # Пустой запрос
        self.Empty_Request('AutoRefClaim_3') # Пустой запрос

        try:
            HPV = int(self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['friend_claim'])

            if HPV:
                if self.Referal_Claim():
                    self.Logging('Success', '🟢', f'Монеты за рефералов собраны! +{HPV:,}')
                    sleep(randint(3, 6)) # Промежуточное ожидание
        except:
            pass



    def NFTs(self) -> None:
        '''Пустая функция просмотра NFT'''

        URL_1 = self.Domain + 'nft/market/collections'
        URL_2 = self.Domain + 'nft/market'
        HEADERS_1 = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON_1 = {'hash': self.Hash_Gen([])}
        JSON_2 = {'limit': 20, 'next': 0, 'hash': self.Hash_Gen([{'limit': 20, 'next': 0}])}

        self.Empty_Request('NFTs_1') # Пустой запрос
        self.Empty_Request('NFTs_2') # Пустой запрос
        self.Empty_Request('NFTs_3') # Пустой запрос
        self.HPV_PRO.post(URL_1, headers=HEADERS_1, json=JSON_1, proxies=self.Proxy) # Пустой запрос
        self.HPV_PRO.post(URL_2, headers=HEADERS_1, json=JSON_2, proxies=self.Proxy) # Пустой запрос
        self.Empty_Request('NFTs_4') # Пустой запрос
        self.Empty_Request('NFTs_1') # Пустой запрос
        self.Empty_Request('NFTs_3') # Пустой запрос
        self.HPV_PRO.post(URL_2, headers=HEADERS_1, json=JSON_2, proxies=self.Proxy) # Пустой запрос
        self.HPV_PRO.post(URL_1, headers=HEADERS_1, json=JSON_1, proxies=self.Proxy) # Пустой запрос



    def Get_Tasks(self) -> list:
        '''Получение списка заданий'''

        URL = self.Domain + 'task-list'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'hash': self.Hash_Gen([])}

        self.Empty_Request('AutoTasks_3') # Пустой запрос

        try:
            HPV = self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()

            TASKS = []

            for Task in HPV:
                if Task['status'] == 'possible':
                    TASKS.append({'ID': Task['id'], 'NAME': Task['name']})

            return TASKS
        except:
            return []



    def Start_Tasks(self, ID: int) -> bool:
        '''Выполнение заданий'''

        URL = self.Domain + 'task-list/complete'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'id': ID, 'hash': self.Hash_Gen([{'id': ID}])}

        self.Empty_Request('AutoTasks_4') # Пустой запрос

        try:
            HPV = self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()
            return True if HPV['task']['status'] == 'granted' else False
        except:
            return False



    def Daily_Reward(self) -> bool:
        '''Получение ежедневной награды'''

        URL = self.Domain + 'grant-day/claim'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'user_auth': self.TG_ID, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://mmbump.pro', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'referer': 'https://mmbump.pro/', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'hash': self.Hash_Gen([])}

        self.Empty_Request('AutoTasks_5') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['day_grant_first']
            return True
        except:
            return False



    def AutoTasks(self, Daily_Reward: int) -> None:
        '''Автоматическое выполнение заданий'''

        try:
            self.Empty_Request('AutoTasks_1') # Пустой запрос
            self.Empty_Request('AutoTasks_2') # Пустой запрос
            self.Empty_Request('AutoTasks_6') # Пустой запрос

            # Выполненине заданий
            Tasks = self.Get_Tasks() # Список заданий
            sleep(randint(3, 5)) # Промежуточное ожидание

            for Task in Tasks:
                if self.Start_Tasks(Task['ID']):
                    self.Logging('Success', '⚡️', f'Задание с {Task["NAME"]} выполнено!')
                sleep(randint(5, 9)) # Промежуточное ожидание

            # Получение ежедневной награды
            if not Daily_Reward or Daily_Reward < int(time()):
                self.Empty_Request('AutoTasks_7') # Пустой запрос
                self.Empty_Request('AutoTasks_8') # Пустой запрос
                self.Empty_Request('AutoTasks_9') # Пустой запрос
                self.Empty_Request('AutoTasks_10') # Пустой запрос
                self.Empty_Request('AutoTasks_11') # Пустой запрос
                self.Empty_Request('AutoTasks_12') # Пустой запрос
                self.Empty_Request('AutoTasks_13') # Пустой запрос

                if self.Daily_Reward():
                    self.Logging('Success', '🎁', 'Ежедневная награда получена!')
                sleep(randint(5, 9)) # Промежуточное ожидание
        except:
            pass



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Token:
                    INFO = self.Get_Info()
                    self.Empty_Request('Authentication_12') # Пустой запрос
                    self.Empty_Request('Authentication_13') # Пустой запрос
                    self.Empty_Request('Authentication_14') # Пустой запрос
                    self.Empty_Request('Authentication_15') # Пустой запрос
                    self.Empty_Request('Authentication_16') # Пустой запрос
                    self.Empty_Request('Authentication_17') # Пустой запрос
                    self.Empty_Request('Authentication_18') # Пустой запрос
                    self.Empty_Request('Authentication_19') # Пустой запрос

                    Balance = INFO['Balance'] # Баланс
                    Boost = INFO['Boost'] # Наличие купленного буста
                    Daily_Reward = INFO['Daily_Reward'] # Ежедневная награда
                    Start_Farm = INFO['Start_Farm'] # Начало фарма
                    self.Logging('Success', '💰', f'Текущий баланс: {Balance}')
                    sleep(randint(3, 5)) # Промежуточное ожидание


                    # Проверка на недавний фарм
                    if Start_Farm:
                        if (datetime.fromtimestamp(Start_Farm) + timedelta(seconds=6*60*60)) > datetime.now():
                            _Waiting = randint(10*60*60, 13*60*60) # Значение времени в секундах для ожидания
                            Waiting_STR = (datetime.fromtimestamp(Start_Farm) + timedelta(seconds=_Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                            self.Logging('Warning', '⏳', f'Сбор уже производился! Следующий сбор: {Waiting_STR}!')

                            # Ожидание конца майнинга
                            _Waiting_For_Upgrade = int(_Waiting / (60*30))
                            for _ in range(_Waiting_For_Upgrade):
                                if HPV_Upgrade_Alert(self.AUTO_UPDATE): # Проверка наличия обновления
                                    return
                                sleep(60*30)
                            sleep(_Waiting - (_Waiting_For_Upgrade * 60 * 30))
                            self.ReAuthentication() # Повторная аутентификация аккаунта
                            continue


                    # Автоматический фарм
                    self.AutoFarm()
                    sleep(randint(3, 5)) # Промежуточное ожидание


                    # Рандомное выполнение действий
                    Autos = [lambda: self.AutoBuyBoost(Boost), self.AutoRefClaim, self.NFTs, lambda: self.AutoTasks(Daily_Reward)]
                    shuffle(Autos) # Перемешивание списока функций
                    for Auto in Autos:
                        Auto() # Запуск случайных действий: покупка буста, сбор монет за рефералов, пустая функция просмотра NFT и выполнение заданий
                        sleep(randint(3, 5)) # Промежуточное ожидание


                    Waiting = randint(10*60*60, 13*60*60) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                    self.Logging('Success', '💰', f'Текущий баланс: {self.Get_Info()["Balance"]}')
                    self.Logging('Warning', '⏳', f'Следующий сбор: {Waiting_STR}!')


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




















def HPV_Main(COINS: list[int], BUY_BOOST: bool, AUTO_UPDATE: bool) -> None:
    '''Запуск BUMP'''

    if s_name() == 'Windows':
        sys(f'cls && title HPV BUMP - V{VERSION}')
    else:
        sys('clear')

    while True:
        HPV_Banner() # Вывод баннера
        HPV_Config_Check(AUTO_UPDATE) # Проверка конфига на валидность
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка конфига окончена... Скрипт запустится через 5 секунд...\n'); sleep(5)

        Console_Lock = Lock()
        Threads = [] # Список потоков

        def Start_Thread(Name: str, URL: str, Proxy: dict, Headers: dict) -> None:
            BUMP = HPV_BUMP(Name, URL, Proxy, Headers, COINS, BUY_BOOST, AUTO_UPDATE, Console_Lock)
            BUMP.Run()

        # Получение конфигурационных данных и запуск потоков
        for Account in HPV_Get_Config(_print=False):
            HPV = Thread(target=Start_Thread, args=(Account['Name'], Account['URL'], Account['Proxy'], Account['Headers'],))
            HPV.start()
            Threads.append(HPV)

        for thread in Threads:
            thread.join()






