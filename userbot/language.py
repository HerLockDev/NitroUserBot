# NEON candi gerisi yalandi


from . import LANGUAGE, LOGS, bot, PLUGIN_CHANNEL_ID
from json import loads, JSONDecodeError
from os import path, remove
from telethon.tl.types import InputMessagesFilterDocument

pchannel = bot.get_entity(PLUGIN_CHANNEL_ID)
LOGS.info("Dil faylı yüklenir...")
LANGUAGE_JSON = None

for dil in bot.iter_messages(pchannel, filter=InputMessagesFilterDocument):
    if ((len(dil.file.name.split(".")) >= 2) and (
            dil.file.name.split(".")[1] == "nitrojson")):
        if path.isfile(f"./userbot/language/{dil.file.name}"):
            try:
                LANGUAGE_JSON = loads(
                    open(
                        f"./userbot/language/{dil.file.name}",
                        "r").read())
            except JSONDecodeError:
                dil.delete()
                remove(f"./userbot/language/{dil.file.name}")

                if path.isfile("./userbot/language/DEFAULT.nitrojson"):
                    LOGS.warn("Varsayılan dil faylı işledilir...")
                    LANGUAGE_JSON = loads(
                        open(
                            f"./userbot/language/DEFAULT.nitrojson",
                            "r").read())
                else:
                    raise Exception("Dil faylı sehfdir.")
        else:
            try:
                DOSYA = dil.download_media(file="./userbot/language/")
                LANGUAGE_JSON = loads(open(DOSYA, "r").read())
            except JSONDecodeError:
                dil.delete()
                if path.isfile("./userbot/language/DEFAULT.nitrojson"):
                    LOGS.warn("Varsayıl dil faylı işledilir...")
                    LANGUAGE_JSON = loads(
                        open(
                            f"./userbot/language/DEFAULT.nitrojson",
                            "r").read())
                else:
                    raise Exception("Dil faylı sehfdir.")
        break

if LANGUAGE_JSON is None:
    if path.isfile(f"./userbot/language/{LANGUAGE}.nitrojson"):
        try:
            LANGUAGE_JSON = loads(
                open(
                    f"./userbot/language/{LANGUAGE}.nitrojson",
                    "r").read())
        except JSONDecodeError:
            raise Exception("Sehf json faylı")
    else:
        if path.isfile("./userbot/language/DEFAULT.nitrojson"):
            LOGS.warn("Varsayılan dil faylı işledilir...")
            LANGUAGE_JSON = loads(
                open(
                    f"./userbot/language/DEFAULT.nitrojson",
                    "r").read())
        else:
            raise Exception(f"{LANGUAGE} faylı tapılmadı")

LOGS.info(f"{LANGUAGE_JSON['LANGUAGE']} dili yüklendi.")


def get_value(plugin=None, value=None):
    global LANGUAGE_JSON

    if LANGUAGE_JSON is None:
        raise Exception("İlk önce dil faylını yükleyin")
    else:
        if plugin is not None or value is None:
            Plugin = LANGUAGE_JSON.get("STRINGS").get(plugin)
            if Plugin is None:
                raise Exception("Sehf plugin")
            else:
                String = LANGUAGE_JSON.get("STRINGS").get(plugin).get(value)
                if String is None:
                    return Plugin
                else:
                    return String
        else:
            raise Exception("Invalid plugin or string")
