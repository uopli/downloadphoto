from pathlib import Path
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.messages import GetMessagesRequest
from telethon.tl.functions.channels import ReadHistoryRequest
from telethon import TelegramClient, errors
import asyncio


class Library:
    MrPhpInfo_cm = 276505
    MrPhpInfo_ct = "5d4e2ae3033eee4aff7a614f937b379b"

    def __init__(self):
        print("Start")

    async def JoinChannel(self, ChannelUsrname):
        paths = list(Path('Activesession').glob('**/*.session'))
        for x in paths:
            _Client = TelegramClient("Activesession/" + str(x.stem), self.MrPhpInfo_cm, self.MrPhpInfo_ct)
            await _Client.connect()
            if await _Client.is_user_authorized():
                await _Client.start()
                print("ok " + str(x.stem))
                await _Client(JoinChannelRequest(ChannelUsrname))
            if not await _Client.is_user_authorized():
                x.unlink()
                print("Delted")

    async def JoinPrivateChannel(self, ChannelLink):
        paths = list(Path('Activesession').glob('**/*.session'))
        for x in paths:
            _Client = TelegramClient("Activesession/" + str(x.stem), self.MrPhpInfo_cm, self.MrPhpInfo_ct)
            await _Client.connect()
            if await _Client.is_user_authorized():
                try:
                    print("ok")
                    await _Client.start()
                    await _Client(ImportChatInviteRequest(ChannelLink))
                    await _Client.send_message(-1001434083094, "جوین شدم")
                except Exception as e:
                    e
            if not await _Client.is_user_authorized():
                x.unlink()
                print("Delted")

    async def startbot(self,phonenumber):
        _Client = TelegramClient("Activesession/" + str(phonenumber), self.MrPhpInfo_cm, self.MrPhpInfo_ct)
        await _Client.connect()
        if await _Client.is_user_authorized():
            try:
                print("ok")
                await _Client.start()
                await _Client.send_message("ChocolateOzvBot", "/start")
                await _Client(JoinChannelRequest("ChocolatePost"))
                await _Client(JoinChannelRequest("ChocolateOzv"))
                await _Client(ImportChatInviteRequest("BA4MtBLRtro3OTA0"))
                await _Client.send_message(-1001434083094, "ربات استارت کانال ربات جوین شدم")
            except Exception as e:
                e
        if not await _Client.is_user_authorized():
            x.unlink()
            print("Delted")

    async def apiJoinChannel(self, message_id):
        paths = list(Path('Activesession').glob('**/*.session'))
        for x in paths:
            _Client = TelegramClient("Activesession/" + str(x.stem), self.MrPhpInfo_cm, self.MrPhpInfo_ct)
            await _Client.connect()
            if await _Client.is_user_authorized():
                try:
                    await _Client.start()
                    await _Client.get_dialogs()
                    getmsg = await _Client.get_messages('ChocolateOzv', ids=[message_id], limit=1)
                    await _Client(ReadHistoryRequest('ChocolateOzv',message_id))
                    geturl = getmsg[0].reply_markup.rows[0].buttons[0].url.split("https://t.me/joinchat/")
                    await _Client(ImportChatInviteRequest(geturl[1]))
                    await _Client.send_message(-1001434083094, "جوین شدم")
                    await getmsg[0].click(2)
                    await _Client.send_message(-1001434083094, "سکه گرفتم")
                    await _Client.disconnect()
                except errors.UserAlreadyParticipantError as e:
                    print("User Has Been Joined This Channel")
                    await _Client.disconnect()
                except Exception as e:
                    await _Client.disconnect()
                    if "object has no attribute" in str(e):
                        break
            if not await _Client.is_user_authorized():
                x.unlink()
                print("Delted")
