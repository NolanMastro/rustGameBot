import asyncio
import time
import datetime
from PIL import Image
from rustplus import RustSocket, CommandOptions, Command, ServerDetails, ChatCommand, EntityEventPayload, TeamEventPayload, ChatEventPayload, ProtobufEvent, ChatEvent, EntityEvent, TeamEvent, Emoji


#/turrets to turn on all turrets.
#/blue_card shows nearby location to get blue card.
#/red_card shows nearby location to get red card.





async def main():
    info={}




    types = {
                1: "Player",
                2: "Explosion",
                3: "VendingMachine",
                4: "CH47",
                5: "Cargo Ship",
                6: "Locked Crate",
                7: "Vendor",
                8: "Attack Heli"
            }

    options = CommandOptions(prefix="!")
    server_details = ServerDetails(info['ip'],  info['port'], info['playerId'], info['playerToken'])
    socket = RustSocket(server_details, command_options=options)
    await socket.connect()

    print(f"It is {(await socket.get_time()).time} on {info['name']}")
    
    inital_data = await socket.get_info()

    
    def convert_xy_to_grid(x, y, initdata):
        trueSize = initdata.size
        convertedSize = int(trueSize / 146.28571428571428)
        gridLetterIndex = int(x / 146.28571428571428)
        gridNumber = int(convertedSize - y / 146.28571428571428)
        
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        gridLetter = ""
        while gridLetterIndex >= 0:
            gridLetter = alphabet[gridLetterIndex % 26] + gridLetter
            gridLetterIndex = (gridLetterIndex // 26) - 1
        
        return f'{gridLetter}{gridNumber}'

        

    #hi
    @Command(server_details,aliases=["hello", "hey", "HI", "Hi", "hI"])
    async def hi(command : ChatCommand):
        if command.sender_steam_id==76561199149660324:
            await socket.send_team_message(f"Hi, diddy.")
        else:
            try:
                await socket.send_team_message(f"Hi, {command.sender_name}.")
            except:
                await socket.send_team_message("Hi, void name.")
    
    #pop       
    @Command(server_details)
    async def pop(command : ChatCommand):
        server_info = await socket.get_info()
        await socket.send_team_message(f'{server_info.players} players online, {server_info.queued_players} in queue.')
    
    #seed
    @Command(server_details, aliases=["S", "s", "Seed"])
    async def seed(command: ChatCommand):
        await socket.send_team_message("The seed is " + str((await socket.get_info()).seed))      
    
    @Command(server_details, aliases=["Team", "t", "T"])
    async def team(command: ChatCommand):
        team_info = await socket.get_team_info()
        message = ""
        offlineMembers = ""
        for i in range(len(team_info.members)):
            if len(message) > 110:
                await socket.send_team_message(message)
                message = ""

            if team_info.members[i].steam_id == 76561199149660324:
                name = 'diddy'
            else:
                name = team_info.members[i].name
            
            if not team_info.members[i].is_online:
                offlineMembers += name
                offlineMembers += f"{Emoji.HEART}"
            elif team_info.members[i].is_alive:
                message += f'{name}: ALIVE @{convert_xy_to_grid(team_info.members[i].x, team_info.members[i].y, inital_data)}\n'
                message+=f'{Emoji.HEART}'
            else:
                days, hours, minutes = convert_epoch_to_hours(team_info.members[i].death_time)
                message += f'{name}: DEAD @{convert_xy_to_grid(team_info.members[i].x, team_info.members[i].y, inital_data)} {minutes} min ago\n'
                message+=f'{Emoji.SKULL}'
            
        await socket.send_team_message(message)
        if offlineMembers == "":
            pass
        else:
            await socket.send_team_message(f'Offline Members: {offlineMembers}')



    def convert_epoch_to_hours(epoch_timestamp):
        current_time = datetime.datetime.now()
        target_time = datetime.datetime.fromtimestamp(epoch_timestamp)
        time_difference = target_time - current_time

        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        return days, hours, minutes


    @Command(server_details)
    async def setf(command: ChatCommand):
        team_chat = await socket.get_team_chat()
        latest_message = team_chat[-1].message if team_chat else ""
        if latest_message.startswith("!setf"):
            _, number = latest_message.split(maxsplit=1)
            global f_id
            f_id = int(number)
            await socket.send_team_message(f'Set furnace smart switch to {f_id}')
    
    @Command(server_details)
    async def f(command: ChatCommand):
        try:
            print(f_id)
            switch_info = await socket.get_entity_info(f_id)
            if switch_info.value:
                await socket.set_entity_value(f_id, False)
                await socket.send_team_message('Furnaces off.')
            else:
                await socket.set_entity_value(f_id, True)
                await socket.send_team_message('Furnaces on.')
        except:
            await socket.send_team_message('The Id of the smart switch isnt set, use !setf id')
            
        

    @Command(server_details)
    async def monitorf(command: ChatCommand):
        team_chat = await socket.get_team_chat()
        latest_message = team_chat[-1].message if team_chat else ""
        if latest_message.startswith("!monitorf"):
            _, number = latest_message.split(maxsplit=1)
            global fm_id
            fm_id = int(number)
            try:
                print(f_id)
                await socket.send_team_message(f'Monitoring current furnace setup. ID of switch: {f_id} Chest ID: {fm_id}')
                async def check_items():
                    while True:
                        recent_chest_info = await socket.get_entity_info(fm_id)
                        await asyncio.sleep(10)

                        new_chest_info = await socket.get_entity_info(fm_id)

                        if recent_chest_info.items[-1].quantity == new_chest_info.items[-1].quantity:
                            await socket.send_team_message('Furnaces are not cooking. Turning switch off.')
                            await socket.set_entity_value(f_id, False)
                        else:
                            print('Furnaces are cooking!')
                asyncio.create_task(check_items())
            except:
                await socket.send_team_message('The Id of the smart switch isnt set, use !setf id')


    

    
            

    #run on start events

    async def watchForDeaths(): # may need work.
        reported_deaths = set()
        while True:
            team_info = await socket.get_team_info()
            for i in range(len(team_info.members)):
                if team_info.members[i].is_alive:
                    try:
                        reported_deaths.discard(team_info.members[i].steam_id)
                        continue
                    except:
                        continue
                if team_info.members[i].steam_id not in reported_deaths:
                    reported_deaths.add(team_info.members[i].steam_id)
                    name = 'dany' if team_info.members[i].steam_id == 76561199149660324 else team_info.members[i].name
                    await socket.send_team_message(f'{name} is dead @{convert_xy_to_grid(team_info.members[i].x, team_info.members[i].y, inital_data)}')
            await asyncio.sleep(10)

    asyncio.create_task(watchForDeaths())








    
    await socket.hang()
    await socket.disconnect()

asyncio.run(main())
