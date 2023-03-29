from telethon import Button
from .Strings import ButtonStrings

class TextButtons:
    # admin panel for setting bot
    ADMIN_PANEL = [
        [Button.text(ButtonStrings.BOT_STATUS, resize=True, single_use=True)],
        [Button.text(ButtonStrings.CHANNEL_SETTING_PANEL, resize=True, single_use=True), Button.text(ButtonStrings.ADMIN_SETTING_PANEL, resize=True, single_use=True)],
        [Button.text(ButtonStrings.SENDER_PANEL, resize=True, single_use=True)],
        [Button.text(ButtonStrings.CLOSE_ADMIN_PANEL, resize=True, single_use=True)]
    ]

    # admin setting panel for add/remove admin and show admins list
    ADMIN_SETTING = [
        [Button.text(ButtonStrings.ADD_ADMIN, resize=True, single_use=True), Button.text(ButtonStrings.REMOVE_ADMIN, resize=True, single_use=True)],
        [Button.text(ButtonStrings.ADMINS_LIST, resize=True, single_use=True)],
        [Button.text(ButtonStrings.BACK_TO_ADMIN_PANEL, resize=True, single_use=True)]
    ]

    # channel setting panel for add/remove channel and show channel list
    CHANNEL_SETTING = [
        [Button.text(ButtonStrings.ADD_CHANNEL, resize=True, single_use=True),Button.text(ButtonStrings.REMOVE_CHANNEL, resize=True, single_use=True)],
        [Button.text(ButtonStrings.CHANELLS_LIST, resize=True, single_use=True)],
        [Button.text(ButtonStrings.BACK_TO_ADMIN_PANEL, resize=True, single_use=True)]
    ]

    # sender panel for send/forward message to all
    SENDER_PANEL = [
        [Button.text(ButtonStrings.FORWARD_TO_ALL, resize=True, single_use=True), Button.text(ButtonStrings.SEND_TO_ALL, resize=True, single_use=True)],
        [Button.text(ButtonStrings.BACK_TO_ADMIN_PANEL, resize=True, single_use=True)]
    ]

    # cancel get or ...(procec)
    CHANEL_PROCEC = [
        [Button.text(ButtonStrings.CHANCEL_PROCEC, resize=True, single_use=True)]
    ]