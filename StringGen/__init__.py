import logging
import pyromod #type: ignore

from pymongo import AsyncMongoClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode

import config

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("oldpyro").setLevel(logging.ERROR)
logging.getLogger("telethon").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

mongo = MongoCli(config.MONGO_DB_URI)
db = mongo.StringGen


class Anony(Client):
    def __init__(self):
        super().__init__(
            name="Anonymous",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            lang_code="en",
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
        )

    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention
        try:
            await mongo.aconnect()
            await mongo.admin.command("ping")
        except Exception as e:
            raise e

    async def stop(self):
        await super().stop()
        await mongo.close()


anony = Anony()
