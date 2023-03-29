# in the name of god | ya ali(ra)
from json import dumps, loads
from os import path

FileList = ['AdminList', 'Channels', 'Users']  # file list for create
Data = {}

for i in FileList:  # create files
    if not path.exists(f'Database/Data/{i}.json'):
        open(f'Database/Data/{i}.json', 'a+').close()

for i in FileList:  # import data
    Data[i] = loads(open(f'Database/Data/{i}.json', 'r').read())


class Database:
    # Channels Pack
    async def add_channel(ChannelID):
        if isinstance(ChannelID,int):
            Data['Channels']['ChannelsID'].append(ChannelID)
            open('Database/Data/Channels.json', 'w').write(dumps(Data["Channels"], indent=4))
        else:
            print('ChannelID not int')

    async def del_channel(ChannelID):
        if isinstance(ChannelID,int):
            Data['Channels']['ChannelsID'].remove(int(ChannelID))
            open('Database/Data/Channels.json', 'w').write(dumps(Data["Channels"], indent=4))
        else:
            print('ChannelID not int')


    async def channel_list():
        ChannelList = Data["Channels"]["ChannelsID"]
        return ChannelList

    # Admins Pack
    async def add_admin(UserID):
        if isinstance(UserID, int):
            Data["AdminList"]["Admins"].append(UserID)
            open('Database/Data/AdminList.json', 'w').write(dumps(Data["AdminList"], indent=4))
        else:
            print('UserID not int')

    async def del_admin(UserID):
        if isinstance(UserID, int):
            Data["AdminList"]["Admins"].remove(UserID)
            open('Database/Data/AdminList.json', 'w').write(dumps(Data["AdminList"], indent=4))
        else:
            print('UserID not int')

    async def admin_list():
        return Data["AdminList"]["Admins"]

    
    # User Pack
    async def add_user_to_database(UserID):
        if UserID not in Data["Users"]["Users"] and str(UserID).isnumeric():
            Data["Users"]["Users"].append(int(UserID))
            open('Database/Data/Users.json', 'w').write(dumps(Data['Users'], indent=4))
        else:
            return False
            
    async def user_list():
        return Data['Users']['Users']

