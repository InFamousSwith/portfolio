import logging
import os

import config
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

simlog = logging.getLogger("ParserLogger")


async def dump_all_messages(channel, client: TelegramClient, image_job: bool):
    """Записывает словарь с информацией о всех сообщениях канала/чата
    Сохраняет изображения, которые мапятся по id c сообщением"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз
    all_messages = []  # список всех сообщений
    total_messages = 0
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    while True:
        history = await client(
            GetHistoryRequest(
                peer=channel,
                offset_id=offset_msg,
                offset_date=None,
                add_offset=0,
                limit=limit_msg,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            if message.to_dict()["id"] % 1000 == 0:
                simlog.info(message.to_dict()["id"])
            idid = str(message.to_dict()["id"])
            if image_job:
                await client.download_media(message, os.path.join(config.IMGS_PATH, f"parsed_jpg_{idid}"))
            all_messages.append(message.to_dict())
            # break
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    return all_messages


async def main(client: TelegramClient, url: str, image_job: bool):
    simlog.info("parser works ...")
    channel = await client.get_entity(url)
    all_messages = await dump_all_messages(channel, client, image_job)
    return all_messages


def clean_images(path: str) -> None:
    if os.listdir(path):
        for image in os.listdir(path):
            os.remove(os.path.join(path, image))


def check_dir(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        clean_images(path)


def parse_channel_job(url, image_job: bool) -> list:
    simlog.info("parse_channel_job works ...")
    api_id = config.API_ID
    api_hash = config.API_HASH
    phone = config.PHONE
    client = TelegramClient(phone, api_id, api_hash)
    client.start()

    check_dir(config.IMGS_PATH)
    with client:
        all_messages = client.loop.run_until_complete(main(client, url, image_job))
    assert all_messages, simlog.info("Messages weren't parsed")
    simlog.info("Messages are parsed")
    return all_messages


# if __name__ == "__main__":
#     all_messages = parse_channel_job("https://t.me/bcsinvestidea", False)
#     print(all_messages[0])
