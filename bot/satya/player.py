import os
import re
import time
import ffmpeg
import asyncio
from os import path
from asyncio import sleep
from config import Config
from youtube_dl import YoutubeDL
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pytgcalls import GroupCallFactory
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMINS = Config.ADMINS
CHAT_ID = Config.CHAT_ID
USERNAME = Config.BOT_USERNAME
ADMINS = Config.ADMINS
USERNAME = Config.BOT_USERNAME
REPLY_MESSAGE = Config.REPLY_MESSAGE

User = Client(
    Config.SESSION_STRING,
    Config.API_ID,
    Config.API_HASH
)

STREAM = {6}
VIDEO_CALL = {}

ydl_opts = {
        "geo_bypass": True,
        "nocheckcertificate": True,
}
ydl = YoutubeDL(ydl_opts)
group_call_factory = GroupCallFactory(User, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)

@Client.on_message(filters.command(["stream", f"stream@{USERNAME}"]) & (filters.chat(CHAT_ID) | filters.private))
async def stream(client, m: Message):
    if 1 in STREAM:
        await m.reply_text("use /endstream**")
        return

    media = m.reply_to_message
    if not media and not ' ' in m.text:
        await m.reply("❗ __Send Me An YouTube Video Link / Live Stream Link / Reply To An Video To Start Streaming!__")

    elif ' ' in m.text:
        msg = await m.reply_text("🔄 `Processing ...`")
        text = m.text.split(' ', 1)
        query = text[1]
        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex,query)
        if match:
            await msg.edit("🔄 `Starting YouTube Stream ...`")
            try:
                meta = ydl.extract_info(query, download=False)
                formats = meta.get('formats', [meta])
                for f in formats:
                        ytstreamlink = f['url']
                ytstream = ytstreamlink
            except Exception as e:
                await msg.edit(f"❌ **YouTube Download Error!** \n\n`{e}`")
                return
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(CHAT_ID)
                await group_call.start_video(ytstream)
                VIDEO_CALL[CHAT_ID] = group_call
                await msg.edit(f"▶️ **Started [YouTube Streaming]({ytstream})!**", disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
        else:
            await msg.edit("🔄 `Starting Live Stream ...`")
            livestream = query
            await sleep(2)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(CHAT_ID)
                await group_call.start_video(livestream)
                VIDEO_CALL[CHAT_ID] = group_call
                await msg.edit(f"▶️ **Started [Live Streaming]({livestream})!**", disable_web_page_preview=True)
                try:
                    STREAM.remove(0)
                except:
                    pass
                try:
                    STREAM.add(1)
                except:
                    pass
            except Exception as e:
                await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")

    elif media.video or media.document:
        msg = await m.reply_text("🔄 `Downloading ...`")
        video = await client.download_media(media)
        await sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(CHAT_ID)
            await group_call.start_video(video)
            VIDEO_CALL[CHAT_ID] = group_call
            await msg.edit("▶️ **Started Streaming!**")
            try:
                STREAM.remove(0)
            except:
                pass
            try:
                STREAM.add(1)
            except:
                pass
        except Exception as e:
            await msg.edit(f"❌ **An Error Occoured!** \n\nError: `{e}`")
    else:
        await m.reply_text("❗ __Send Me An Live Stream Link / YouTube Video Link / Reply To An Video To Start Streaming!__")
        return


@Client.on_message(filters.command(["endstream", f"endstream@{USERNAME}"]) & (filters.chat(CHAT_ID) | filters.private))
async def endstream(client, m: Message):
    if 0 in STREAM:
        await m.reply_text("use /stream first")
        return
    try:
        await VIDEO_CALL[CHAT_ID].stop()
        await m.reply_text("⏹️ **Stopped Streaming!**")
        try:
            STREAM.remove(1)
        except:
            pass
        try:
            STREAM.add(0)
        except:
            pass
    except Exception as e:
        await m.reply_text(f"❌ **An Error Occoured!** \n\nError: `{e}`")
