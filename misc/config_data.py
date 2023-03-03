"""
This class is using for work with env variables
"""


from dataclasses import dataclass
from environs import Env

MIG_URL = "https://mig.kz/"
API_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/"


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]


@dataclass
class Api:
    mig_api: str
    google_api: str


@dataclass
class Config:
    tg_bot: TgBot
    apis: Api


def load_config(path: str) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  apis=Api(MIG_URL, API_URL))
