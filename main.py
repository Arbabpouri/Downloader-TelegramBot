#                                                in the name of god
#github : https://github.com/Arbabpouri
# It may have bugs because it has not been fully tested
from asyncio import sleep
from json import loads
from Database.Database import Database
import jdatetime
import logging
from re import match
from telethon.tl.types import PeerUser, PeerChannel
from telethon.tl.functions.channels import GetParticipantRequest, GetFullChannelRequest
from telethon.errors import ChannelPrivateError, ChatAdminRequiredError, UserNotParticipantError
from telethon.sync import TelegramClient, Button, custom
from telethon.events import NewMessage, CallbackQuery
from modules.Buttons import TextButtons, InlineButton
from modules.download import YoutubeDownloader, InstagramDownloader, PinterestDownloader, SpotifyDownloader
from Config import client
logging.basicConfig(filename="log.txt", filemode="a",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

AdminResponsive, UserResponsive, SendMessageList, ForwardMessageList = [], [], [], []
print('Imported data')
# ------------------------------------------------------ Body Bot --------------------------------------------------------------
# ---------------------------------------------------- Creator pack ------------------------------------------------------------


async def admins_check(event):
    if event.is_private and event.sender_id in await Database.admin_list() and event.sender_id not in AdminResponsive and event.sender_id not in UserResponsive:
        return True
    else:
        return False


async def users_check(event):
    if event.is_private and event.sender_id not in AdminResponsive and event.sender_id not in UserResponsive:
        return True
    else:
        return False


async def get_link_check(event):
    if event.is_private and event.sender_id in UserResponsive and event.sender_id not in AdminResponsive:
        return True
    else:
        return False


async def forced_to_join(UserID):
    Channels_ID = await Database.channel_list()
    if Channels_ID == []:
        return True
    elif str(UserID).isnumeric():
        try:
            NoJoin = []
            for i in Channels_ID:
                try:
                    Channel = await client.get_entity(PeerChannel(i))
                    await client(GetParticipantRequest(Channel, PeerUser(int(UserID))))
                except UserNotParticipantError:
                    ChannelLink = await client(GetFullChannelRequest(Channel))
                    NoJoin.append(ChannelLink.full_chat.exported_invite.link)
                except ChatAdminRequiredError:
                    await Database.del_channel(int(i))
                    Admins = await Database.admin_list()
                    for ii in Admins:
                        await client.send_message(PeerUser(ii), f'چنل با ایدی عددی __{i}__ از لیست چنل ها حذف شد زیرا ربات را از ادمینی دراورده بود')
                    if Channels_ID == []:
                        return True

            if NoJoin != []:
                Buttons, Num = [], 1
                for i in NoJoin:
                    Buttons.append([Button.url(f'عضویت در کانال {str(Num)}', str(i))])
                    Num += 1
                Buttons.append([Button.inline('جوین شدم', 'check')])
                await client.send_message(PeerUser(int(UserID)), 'برای تایید شدن عضو شید', buttons=Buttons)
                return False
            else:
                return True
        except Exception as ex:
            print(ex)
    else:
        print('UserID not numeric or type(Channels_ID) is not list')


async def send_to_all(Admin_User_ID, MessageForSend, UserIDList):
    if SendMessageList == []:
        SendMessageList.append(MessageForSend)
        while True:
            await client.send_message(PeerUser(int(Admin_User_ID)), SendMessageList[0])
            await client.send_message(PeerUser(int(Admin_User_ID)), f"⏳ تقریبی برای ارسال پیام بالا 👆🏻 حدود <code>{len(UserIDList) * 0.2 + 10}</code> ثانیه طول میکشد.\n\n🙏🏻 لطفا صبور باشید.\n\n♨️ اگر قصد ارسال چندین پیام دیگر نیز دارید , مجدد ارسال کنید تا در لیست انتظار ذخیره شوند و به نوبت ارسال میشوند.\n\n🆔 @DownloadYarRobot", parse_mode='html')
            Number, Error = 0, 0
            await sleep(10)
            for i in UserIDList:
                try:
                    await client.send_message(PeerUser(int(i)), SendMessageList[0])
                    Number += 1
                    await sleep(0.2)
                except Exception as ex:
                    Error += 1
            await client.send_message(PeerUser(int(Admin_User_ID)), SendMessageList[0])
            SendMessageList.remove(SendMessageList[0])
            await client.send_message(PeerUser(int(Admin_User_ID)), f"⭕️ اعلام وضعیت ارسال همگانی 💢\n\n✅ وضعیت پیام های ارسال شده : پیام بالا 👆🏻 برای <code>{Number}</code> نفر از کاربران ارسال شد.\n\n❌ وضعیت پیام های ارسال نشده : پیام بالا 👆🏻 برای <code>{Error}</code> نفر از کاربران ارسال نشد.\n\n🪑 وضعیت پیام های در انتظار : تعداد <code>{len(SendMessageList)}</code> پیام در لیست انتظار برای ارسال باقی مانده اند.\n\n🆔 @DownloadYarRobot", parse_mode='html')
            Number, Error = 0, 0
            if SendMessageList == []:
                break
        
    else:
        await client.send_message(PeerUser(int(Admin_User_ID)), f"✅ پیام ارسالی شما به لیست انتظار افزوده شد.\n\n🪑 وضعیت پیام های در انتظار : تعداد <code>{len(SendMessageList)}</code> پیام در لیست انتظار برای ارسال باقی مانده اند.\n\n🆔 @DownloadYarRobot", parse_mode='html')
        SendMessageList.append(MessageForSend)


async def forward_to_all(Admin_User_ID, MessageForSend, UserIDList):
    if ForwardMessageList == []:
        ForwardMessageList.append(MessageForSend)
        while True:
            Number, Error = 0, 0
            await client.send_message(PeerUser(int(Admin_User_ID)), ForwardMessageList[0])
            await client.send_message(PeerUser(int(Admin_User_ID)), f"⏳ تقریبی برای ارسال پیام بالا 👆🏻 حدود <code>{len(UserIDList) * 5 + 10}</code> ثانیه طول میکشد.\n\n🙏🏻 لطفا صبور باشید.\n\n♨️ اگر قصد ارسال چندین پیام دیگر نیز دارید , مجدد ارسال کنید تا در لیست انتظار ذخیره شوند و به نوبت ارسال میشوند.\n\n🆔 @DownloadYarRobot", parse_mode='html')
            await sleep(10)
            for i in UserIDList:
                try:
                    await client.forward_messages(PeerUser(int(i)), ForwardMessageList[0])
                    Number += 1
                    await sleep(5)
                except Exception as ex:
                    Error += 1
            await client.send_message(PeerUser(int(Admin_User_ID)), ForwardMessageList[0])
            ForwardMessageList.remove(ForwardMessageList[0])
            await client.send_message(PeerUser(int(Admin_User_ID)), f"⭕️ اعلام وضعیت فوروارد همگانی 💢\n\n✅ وضعیت پیام های ارسال شده : پیام بالا 👆🏻 برای <code>{Number}</code> نفر از کاربران ارسال شد.\n\n❌ وضعیت پیام های ارسال نشده : پیام بالا 👆🏻 برای <code>{Error}</code> نفر از کاربران ارسال نشد.\n\n🪑 وضعیت پیام های در انتظار : تعداد <code>{len(ForwardMessageList)}</code> پیام در لیست انتظار برای ارسال باقی مانده اند.\n\n🆔 @DownloadYarRobot", parse_mode='html')
            Number, Error = 0, 0
            if ForwardMessageList == []:
                break
        
    else:
        await client.send_message(PeerUser(int(Admin_User_ID)), f"✅ پیام ارسالی شما به لیست انتظار افزوده شد.\n\n🪑 وضعیت پیام های در انتظار : تعداد <code>{len(ForwardMessageList)}</code> پیام در لیست انتظار برای ارسال باقی مانده اند.\n\n🆔 @DownloadYarRobot", parse_mode='html')
        ForwardMessageList.append(MessageForSend)


async def second_to_date(Time:float):
    ElapsedTime = {
        "D":0,
        "H":0,
        "M":0,
        "S":0
    }
    Date = Time / 60
    while True:
        if Date >= 1440:
            ElapsedTime["D"] += 1
            Date -= 1440

        elif Date < 1440 and Date >= 60:
            ElapsedTime["H"] += 1 
            Date -= 60

        elif Date < 60 and Date > 1:
            ElapsedTime["M"] += 1
            Date -= 1

        elif Date < 1:
            ElapsedTime["S"] = round(Date * 60)
            return ElapsedTime


@client.on(NewMessage(pattern='پنل', func= admins_check))
async def ADMIN_SETTING(event):
    await client.send_message(event.sender_id, 'سلام ادمین عزیز به پنل مدیریت ربات خود خوش امدید 😀', buttons= TextButtons.ADMIN_PANEL)


@client.on(NewMessage(pattern='👥 آمار ربات 👥', func= admins_check))
async def members(event):
    await client.send_message(event.sender_id, f"""👋 سلام {event.chat.first_name} خسته نباشی
💢 امار ربات شما تا این لحظه برابر است با: ⬇️

👥 - تعداد ممبر : <code>{str(len(await Database.user_list()))}</code>
🫂 - تعداد ادمین ها :  <code>{str(len(await Database.admin_list()))}</code>
🗣 - تعداد چنل های قفل شده : <code>{str(len(await Database.channel_list()))}</code>
📅 تاریخ امروز : <b>{str(jdatetime.date.today()).replace('-', '/')}</b>
🕰 ساعت : <b>{str(jdatetime.datetime.now().strftime("%H:%M:%S"))}</b>
🆔 @DownloadYarRobot
""", buttons= TextButtons.ADMIN_PANEL, parse_mode= 'html')

# ----------------------------------------------------- Channel pack ----------------------------------------------------------

@client.on(NewMessage(pattern='📍 بخش چنل 📍', func= admins_check))
async def channel_menu(event):
    await client.send_message(event.sender_id, "به بخش چنل خوش امدید!\nچه کاری میتونم براتون بکنم ؟", buttons= TextButtons.CHANNEL_SETTING)


@client.on(NewMessage(pattern='🧮 افزودن چنل 🧮', func= admins_check))
async def add_channel(event):
    await client.send_message(event.sender_id, f"🌹 خب ببین {event.chat.first_name} کامل گوش بده ببین چی میگم.😎\n✅ برای افزودن قفل چنل باید این کاراییو که میگم  به درستی انجام بدی وگرنه نمیتونم کمکت کنم و شرمندت میشم.😢\n1️⃣ اولین کار اینه که منو (رباتو) توی چنلی که میخوای قفل شه ادمین کنی.\n2️⃣ دومین مرحله اینه که یه پیام (ترجیحا به صورت متن باشه) از همون چنل که منو ادمین کردی توش برام بفرستی تا بتونم مشخصاتشو در بیارم و قفل شم روش.\n3️⃣ قفل میشم روش و میتونی لذت ببری.\n🔴 #تذکر = یادت نره ربات رو از ادمینی در نیاری وگرنه از لیست چنلای قفل شده پاکش میکنم.🔴\n🆔 @DownloadYarRobot", buttons= TextButtons.CHANEL_PROCEC)
    AdminResponsive.append(event.sender_id)
    # give chat id for add to database

    @client.on(NewMessage(func=lambda e: e.is_private and e.sender_id in AdminResponsive))
    async def GiveChannelForAdd(event2):
        if event2.message.message == event.message.message or event.sender_id != event2.sender_id:
            return False
        elif event2.message.message == "❌ کنسل کردن ❌":
            client.remove_event_handler(GiveChannelForAdd)
            AdminResponsive.remove(event2.sender_id)
            await client.send_message(event2.sender_id, "عملیات کنسل شد\n\n\nبه پنل مدیریت بازگشتید", buttons= TextButtons.ADMIN_PANEL)
        elif event2.fwd_from:
            try:
                Channels = await Database.channel_list()
                if int(event2.fwd_from.from_id.channel_id) not in Channels:
                    Link = await client(GetFullChannelRequest(PeerChannel(int(event2.fwd_from.from_id.channel_id))))
                    if Link.full_chat.admins_count != None:
                        client.remove_event_handler(GiveChannelForAdd)
                        await Database.add_channel(int(event2.fwd_from.from_id.channel_id))
                        AdminResponsive.remove(event2.sender_id)
                        await client.send_message(event2.sender_id, f"کانال با ایدی عددی {event2.fwd_from.from_id.channel_id} و لینک {Link.full_chat.exported_invite.link} به لیست چنل های قفل شده اضافه شد :)\n\n\nبه پنل مدیریت بازگشتید", buttons= TextButtons.ADMIN_PANEL)
                    else:
                        await client.send_message(event2.sender_id, "رفیق مثل اینکه منو ادمین کانال نکردی\nلطفا اول منو ادمین کن بعد پیامو فوروارد کن", buttons= TextButtons.CHANEL_PROCEC)
                else:
                    await client.send_message(event2.sender_id, "🤭 این کانال در لیست کانال های قفل شده هست 🤖", buttons= TextButtons.CHANEL_PROCEC)
            except AttributeError:
                await client.send_message(event2.sender_id, "❌ پیام رو از کانال برام بفرست نه از چیز دیگه , فقط و فقط از کانال مورد نظرت 😐", buttons= TextButtons.CHANEL_PROCEC)
            except ChannelPrivateError:
                await client.send_message(event2.sender_id, "❌ هنوز منو توی چنل ادمین نکردی سلطان\nگفتم بهت که اول تو کانال ادمینم کن بعد فوروارد کن ❌", buttons= TextButtons.CHANEL_PROCEC)

            except Exception as ex:
                await client.send_message(event2.sender_id, "❌ هنوز منو توی چنل ادمین نکردی سلطان\nگفتم بهت که اول تو کانال ادمینم کن بعد فوروارد کن ❌", buttons= TextButtons.CHANEL_PROCEC)
        else:
            await client.send_message(event2.sender_id, "❌ جناب برای اضافه کردن کانال به لیست لطفا ابتدا اموزش رو بخونید سپس دست به کار بشید ❌\n⭕️ شما پیام رو از کانال فوروراد نکردید ⭕️", buttons= TextButtons.CHANEL_PROCEC)


@client.on(NewMessage(pattern='🖇 حذف چنل 🖇', func= admins_check))
async def remove_channel(event):
    Pack = {
        "ChannelList": await Database.channel_list(),
        "Channels": "",
        "Num": 0
    }
    if Pack['ChannelList'] != []:
        for i in Pack['ChannelList']:
            Pack['Num'] += 1
            ChannelLink = await client(GetFullChannelRequest(PeerChannel(i)))
            if ChannelLink.full_chat.admins_count != None:
                Pack['Channels'] += f"{Pack['Num']} ) ID : {i} , Link : {ChannelLink.full_chat.exported_invite.link}\n\n"
            else:
                await Database.del_channel(i)
                Pack['ChannelList'].remove(i)
                await client.send_message(event.sender_id, f'چنلی به ایدی عددی {i} از قفل ربات ها برداشته شد زیرا ربات رو ازادمینی دراورده بود')
                if Pack['ChannelList'] == []:
                    await client.send_message(event.sender_id, 'چنلی برای نمایش وجود ندارد')
                    break
        if Pack["ChannelList"] != []:
            await client.send_message(event.sender_id, f"خب یکی ایدی عددی هرکدام از چنل هارا که میخواهید حذف شود وارد کنید\n{Pack['Channels']}", buttons= TextButtons.CHANEL_PROCEC)
            AdminResponsive.append(event.sender_id)
            Pack = 0
            # give channel id for delete from database

            @client.on(NewMessage(func=lambda e: e.is_private and e.sender_id in AdminResponsive))
            async def GiveChannelChatIDForDelete(event2):
                if event2.message.message == event.message.message or event2.sender_id != event.sender_id:
                    return False
                elif event2.message.message == "❌ کنسل کردن ❌":
                    AdminResponsive.remove(event2.sender_id)
                    client.remove_event_handler(GiveChannelChatIDForDelete)
                    await client.send_message(event2.sender_id, "عملیات کنسل شد\n\nبه پنل مدیریت بازگشتید", buttons= TextButtons.ADMIN_SETTING)
                elif event2.message.message.isnumeric():
                    Channels = await Database.channel_list()
                    if int(event2.message.message) in Channels:
                        client.remove_event_handler(GiveChannelChatIDForDelete)
                        await Database.del_channel(int(event2.message.message))
                        AdminResponsive.remove(event2.sender_id)
                        await client.send_message(event2.sender_id, f"کانال با ایدی عددی {event2.message.message} از لیست کانال های قفل شده حذف شد\n\nبه پنل مدیریت بازگشتید", buttons= TextButtons.ADMIN_PANEL)
                    else:
                        await client.send_message(event2.sender_id, "دوست عزیز این ایدی عددی اصلا در لیست وجود ندارد لطفا دقت کنید", buttons= TextButtons.CHANEL_PROCEC)
                else:
                    await client.send_message(event2.sender_id, "لطفا ایدی عددی کانال رو ارسال کنید غیر این چیزی ارسال نکنید", buttons= TextButtons.CHANEL_PROCEC)
        else:
            await client.send_message(event.sender_id, "چنلی برای حذف کردن وجود ندارد جناب", buttons= TextButtons.CHANEL_PROCEC)
    else:
        await client.send_message(event.sender_id, "چنلی برای حذف کردن وجود ندارد جناب", buttons= TextButtons.CHANEL_PROCEC)


@client.on(NewMessage(pattern='🗂 لیست چنل ها 🗂', func= admins_check))
async def channels_list(event):
    Pack = {
        "ChannelList": await Database.channel_list(),
        "Channels": "",
        "Num": 0
    }
    if Pack['ChannelList'] != []:
        for i in Pack['ChannelList']:
            Pack['Num'] += 1
            ChannelLink = await client(GetFullChannelRequest(PeerChannel(i)))
            if ChannelLink.full_chat.admins_count != None:
                Pack['Channels'] += f"{Pack['Num']} ) ID : {i} , Link : {ChannelLink.full_chat.exported_invite.link}\n\n"
            else:
                await Database.del_channel(i)
                await client.send_message(event.sender_id, f'چنلی به ایدی عددی {i} از قفل ربات ها برداشته شد زیرا ربات رو ازادمینی دراورده بود')
                if Pack['ChannelList'] == []:
                    await client.send_message(event.sender_id, 'چنلی برای نمایش وجود ندارد')
                    break

        await client.send_message(event.sender_id, str(Pack['Channels']))
        Pack = 0
    else:
        await client.send_message(event.sender_id, "چنلی برای نمایش وجود ندارد")

# ------------------------------------------------------- Admin pack ------------------------------------------------------------


@client.on(NewMessage(pattern='🪄 بخش ادمین 🪄', func= admins_check))
async def admin_menu(event):
    await client.send_message(event.sender_id, 'به بخش ادمین خوش امدید\n\nچه کاری براتون انجام بدم سرورم', buttons= TextButtons.ADMIN_SETTING)


@client.on(NewMessage(pattern='💥 افزودن ادمین 💥', func= admins_check))
async def add_admin(event):
    await client.send_message(event.sender_id, f"🌹 خب ببین {event.chat.first_name} عزیز , برای اضافه کردن ادمین 2 تا روش داره که الان جفتشو برات توضیح میدم. 🫡\n1️⃣ روش اول ) ایدی عددی کاربر رو بفرستی تا من به ادمینا اضافش کنم. ✅\n🔺 #توجه : باید حتما ایدی عددی رو به صورت عدد بدی نری یوزرنیم رو بفرستی که ناراحت میشم. 🤭\n2️⃣ روش دوم ) یه پیام ازش فوروارد کن برام که اضافش کنم به لیست ادمینا. ✅\n🔺 #توجه : باید کاربر فورواردش باز باشه تا بتونم ایدی عددیشو درارم اگر بسته بهش بگو بازش کنه اگر نمیکنه از روش اول استفاده کن , ماهم اذیت نکن. 😀", buttons= TextButtons.CHANEL_PROCEC)
    AdminResponsive.append(event.sender_id)
    # give admin user id for add to database

    @client.on(NewMessage(func=lambda e: e.is_private and e.sender_id in AdminResponsive))
    async def GetUserIDForAddAdmin(event2: custom.message.Message):
        if event2.message.message == event.message.message or event.sender_id != event2.sender_id:
            return False
        elif event2.message.message == "❌ کنسل کردن ❌":
            client.remove_event_handler(GetUserIDForAddAdmin)
            AdminResponsive.remove(event2.sender_id)
            await client.send_message(event2.sender_id, "عملیات لغو شد\n\nبه پنل بازگشتید", buttons= TextButtons.ADMIN_PANEL)
        elif event2.fwd_from:
            try:
                Admins = await Database.admin_list()
                if int(event2.fwd_from.from_id.user_id) not in Admins:
                    client.remove_event_handler(GetUserIDForAddAdmin)
                    await Database.add_admin(int(event2.fwd_from.from_id.user_id))
                    AdminResponsive.remove(event.sender_id)
                    await client.send_message(event2.sender_id, f"ادمین با ایدی عددی {event2.fwd_from.from_id.user_id} به لیست ادمین ها اضافه شد\n\nبه پنل مدیریت بازگشتید", buttons= TextButtons.ADMIN_SETTING)
                else:
                    await client.send_message(event2.sender_id, "ایشان در لیست ادمین ها حضور دارد", buttons= TextButtons.CHANEL_PROCEC)

            except AttributeError:
                await client.send_message(event2.sender_id, "اوه یه مشکلی پیش اومد\nمیتونه 2 تا دلیل داشته باشه\n1️⃣ پیام رو از شخص نفرستادی و از جای دیگه فوروارد زدی 🤨\n2️⃣ فوروارد شخص بسته است و نمیشه ایدی عددیشو دراورد , پس پیشنهاد من اینه ایدی عددیشو درار بفرست برام تا اضافش کنم , برای این کار میتونی ازین ربات استفاده کنی 🥹\n🆔 @usinfobot", buttons= TextButtons.CHANEL_PROCEC)

        elif event2.message.message.isnumeric():
            try:
                Admins = await Database.admin_list()
                if int(event2.message.message) not in Admins:
                    client.remove_event_handler(GetUserIDForAddAdmin)
                    await Database.add_admin(int(event2.message.message))
                    AdminResponsive.remove(event2.sender_id)
                    await client.send_message(event2.sender_id, f'ادمین با ایدی عددی {str(event2.message.message)} به لیست ادمین ها افزوده شد', buttons= TextButtons.ADMIN_PANEL)
                else:
                    await client.send_message(event2.sender_id, "ایشان در لیست ادمین ها حضور دارد قربان", buttons= TextButtons.CHANEL_PROCEC)
            except ValueError:
                await client.send_message(event2.sender_id, "این ایدی عددی متعلق به کسی نیست و فیکه :)", buttons= TextButtons.CHANEL_PROCEC)
        else:
            await client.send_message(event2.sender_id, "جناب لطفا اموزش رو مطالعه کنید دوباره سپس اقدام کنید , یا پیام رو از شخص فوروراد کنید یا ایدی عددی ایشان رو وارد کنید چیزی خارج از این نباشه", buttons= TextButtons.CHANEL_PROCEC)


@client.on(NewMessage(pattern='🫧 حذف ادمین 🫧', func= admins_check))
async def remove_admin(event):
    global DelAdminText
    DelAdminText = event.message.message
    Pack = {
        "AdminsList": await Database.admin_list(),
        "Admins": "",
        "Num": 0,
    }
    if Pack['AdminsList'] != []:
        for i in Pack['AdminsList']:
            Pack['Num'] += 1
            Pack['Admins'] += f"{Pack['Num']} ) User ID : {i}\n\n"
        await client.send_message(event.sender_id, f"از لیست ادمین ها ایدی عددی را انتخاب کرده و ارسال کنی\nتوجه کنید چیز دیگری جز این نباشد\n\n{Pack['Admins']}", buttons= TextButtons.CHANEL_PROCEC)
        AdminResponsive.append(event.sender_id)
        Pack = 0
        # give admin user id for delete from database

        @client.on(NewMessage(func=lambda e: e.is_private and e.sender_id in AdminResponsive))
        async def GetAdminUserIDForDelete(event2):
            if event2.message.message == event.message.message or event2.sender_id != event.sender_id:
                return False
            elif event2.message.message == "❌ کنسل کردن ❌":
                client.remove_event_handler(GetAdminUserIDForDelete)
                AdminResponsive.remove(event2.sender_id)
                await client.send_message(event2.sender_id, "عملیات لغو شد\n\nبه پنل مدیریت بازگشتید", buttons= TextButtons.ADMIN_SETTING)
            elif event2.message.message.isnumeric():
                Admins = await Database.admin_list()
                if int(event2.message.message) in Admins:
                    client.remove_event_handler(GetAdminUserIDForDelete)
                    await Database.del_admin(int(event2.message.message))
                    AdminResponsive.remove(event2.sender_id)
                    await client.send_message(event2.sender_id, f"ادمین با ایدی عددی {event2.message.message} از لیست ادمین ها حذف شد\n\nبه پنل مدیریت بازگشتید", buttons= TextButtons.ADMIN_PANEL)
                else:
                    await client.send_message(event2.sender_id, f"ادمینی با این ایدی عددی اصلا در لیست ادمین ها حضور ندارد قربان", buttons= TextButtons.CHANEL_PROCEC)

            else:
                await client.send_message(event2.sender_id, f"جناب لطفا ایدی عددی رو ارسال کنید و به شکل عدد باشه فقط :|", buttons= TextButtons.CHANEL_PROCEC)

    else:
        await client.send_message(event.sender_id, "ادمینی وجود ندارد")


@client.on(NewMessage(pattern='❄️ لیست ادمین ها ❄️', func= admins_check))
async def admins_list(event):
    Pack = {
        "AdminsList": await Database.admin_list(),
        "Admins": "",
        "Num": 0,
    }
    if Pack['AdminsList'] != []:
        for i in Pack['AdminsList']:
            Pack['Num'] += 1
            Pack['Admins'] += f"{Pack['Num']} ) User ID : {i}\n\n"
        await client.send_message(event.sender_id, Pack['Admins'])
        Pack = 0
    else:
        await client.send_message(event.sender_id, "ادمینی وجود ندارد")

# ------------------------------------------------------- User pack --------------------------------------------------------------



@client.on(NewMessage(pattern="📣 پیام رسانی 📣", func= admins_check))
async def send_panel_sender(event):
    await client.send_message(event.sender_id, "⚡ فوروارد کنم یا ارسال کنم قربان؟", buttons= TextButtons.SENDER_PANEL)


@client.on(NewMessage(pattern="🖇 پیام همگانی", func= admins_check))
async def send_message_to_all(event):
    AdminResponsive.append(event.sender_id)
    await client.send_message(event.sender_id, "⚠ پیام خود را برای ارسال همگانی , ارسال کنید", buttons= TextButtons.CHANEL_PROCEC)

    @client.on(NewMessage(func=lambda e: e.is_private and e.sender_id in AdminResponsive))
    async def get_message_for_send_all(event2):
        if event2.message.message == event.message.message:
            return False
        elif event2.message.message == "❌ کنسل کردن ❌":
            client.remove_event_handler(get_message_for_send_all)
            AdminResponsive.remove(event2.sender_id)
            await client.send_message(event.sender_id, "❌ عملیات ارسال همگانی کنسل شد", buttons= TextButtons.ADMIN_PANEL)
        else:
            client.remove_event_handler(get_message_for_send_all)
            AdminResponsive.remove(event2.sender_id)
            await send_to_all(event2.sender_id, event2.message, await Database.user_list())


@client.on(NewMessage(pattern="📎 فوروارد همگانی", func= admins_check))
async def forward_message_to_all(event):
    AdminResponsive.append(event.sender_id)
    await client.send_message(event.sender_id, "⚠ پیام خود را برای فوروارد همگانی ارسال کنید", buttons= TextButtons.CHANEL_PROCEC)

    @client.on(NewMessage(func=lambda e: e.is_private and e.sender_id in AdminResponsive))
    async def get_message_for_forward_all(event2):
        if event2.message.message == event.message.message:
            return False
        elif event2.message.message == "❌ کنسل کردن ❌":
            client.remove_event_handler(get_message_for_forward_all)
            AdminResponsive.remove(event2.sender_id)
            await client.send_message(event.sender_id, "❌ عملیات فوروراد همگانی کنسل شد", buttons= TextButtons.ADMIN_PANEL)
        else:
            client.remove_event_handler(get_message_for_forward_all)
            AdminResponsive.remove(event2.sender_id)
            await forward_to_all(event2.sender_id, event2.message, await Database.user_list())


@client.on(NewMessage(pattern='🔙 برگشت 🔙', func= admins_check))
async def back(event):
    await ADMIN_SETTING(event)


@client.on(NewMessage(pattern='❌ بستن پنل مدیر ❌', func= admins_check))
async def close_panel(event):
    await start_panel(event)

# ------------------------------------------------------ User pack -------------------------------------------------------------


@client.on(NewMessage(pattern='/start', func= users_check))
async def start_panel(event):
    await Database.add_user_to_database(event.sender_id)
    if await forced_to_join(event.sender_id):
        await client.send_message(event.sender_id, "😎 سلام به ربات آدور دانلودر خوش اومدی, لینک ویدیو یوتیوب رو ارسال کن تا لینک دانلود بهت بدم و بتونی دانلودش کنی", buttons= Button.clear())


@client.on(CallbackQuery(data='check', func= users_check))
async def check_forced(event):
    if await forced_to_join(event.sender_id):
        await event.delete()
        await start_panel(event)



@client.on(NewMessage(func= users_check))
async def youtube_panel(event):
    if str(event.message.message).lower() == "/start": return False
    elif await forced_to_join(event.sender_id):
        regex = match(r"(.+?)(\/)(watch\x3Fv=)?(embed\/watch\x3Ffeature\=player_embedded\x26v=)?([a-zA-Z0-9_-]{11})+", event.message.message)
        if regex:
            UserResponsive.append(event.sender_id)
            await client.send_message(event.sender_id, '⁉ لطفا صبر کنید')
            Urls = await YoutubeDownloader(str(event.message.message)).youtube_download()
            if Urls != False:
                ButtonsLink = [[Button.inline('🎭 نام', 'nothing'), Button.inline('📍 لینک دانلود', 'nothing')]]
                for i in range(len(Urls)):
                    try:
                        ButtonsLink.append([Button.inline(f'🎞 Video : {str(Urls["formats"][i]["qualityLabel"])}'), Button.url('دانلود',str(Urls["formats"][i]["url"]))])
                    except KeyError:
                        break
                await client.send_message(event.sender_id, 'لینک دانلود ویدیو تقدیم شما 🌹', buttons= ButtonsLink)
                ButtonsLink = None
                UserResponsive.remove(event.sender_id)
            else:
                UserResponsive.remove(event.sender_id)
                await client.send_message(event.sender_id, "❌ لینک ارسالی اشتباه است ❌")



print('Bot is online :)')
client.run_until_disconnected()
