from time import sleep
import asyncio

from telethon import TelegramClient
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest

from config import API_ID, API_HASH, SESSION_NAME, WIDTH, HEIGHT, \
    FONT_SIZE, FONT_PATH, FONT_COLOR, BACKGROUND_COLOR, PHOTO_NAME
from changer import PhotoChanger


client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
client.start()


photo_changer = PhotoChanger(
    WIDTH, HEIGHT, FONT_SIZE, FONT_PATH,
    FONT_COLOR, BACKGROUND_COLOR
)


async def main():
    last_time = photo_changer.time(':')[1]
    while True:
        now = photo_changer.time(':')[1]
        if now != last_time:
            photo_changer.save_profile_photo()
            await client(DeletePhotosRequest(await client.get_profile_photos("me")))
            with open(PHOTO_NAME, 'rb') as photo:
                file = await client.upload_file(photo)
            await client(UploadProfilePhotoRequest(file))
            last_time = now
        sleep(5)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
