import time
import asyncio
from PIL import Image
from utils import verify_name, convert_xy_to_grid, convert_epoch_to_hours, closest_monument, closest_blue_monuments, closest_red_monuments, monuments_readable, grids_apart, event_ids, whatCorner
from rustplus import RustSocket, CommandOptions, Command, ServerDetails, ChatCommand, EntityEventPayload, TeamEventPayload, ChatEventPayload, ProtobufEvent, ChatEvent, EntityEvent, TeamEvent, Emoji

#try to bruteforce electrical item id's?
#heli tracker

async def main():
    info={}





    options = CommandOptions(prefix="!")
    server_details = ServerDetails(info['ip'],  info['port'], info['playerId'], info['playerToken'])
    socket = RustSocket(server_details, command_options=options)
    await socket.connect()

    print(f"It is {(await socket.get_time()).time} on {info['name']}")
    
    inital_data = await socket.get_info()
    map = await socket.get_map_info()
    
    

    #blue
    @Command(server_details)
    async def blue(command: ChatCommand):
        team_info = await socket.get_team_info()
        for member in team_info.members:
            if member.steam_id == command.sender_steam_id:
                sender_x = member.x
                sender_y = member.y
                break
        closeBlueMonuments, closeBlueMonumentsCoordinates = closest_blue_monuments(sender_x,sender_y,map.monuments)                                                                                                                                                                                                                                                                                               #
        await socket.send_team_message(f"The closest places to get a blue card are, {closeBlueMonuments[0]['name']} {grids_apart(convert_xy_to_grid(sender_x,sender_y, inital_data),convert_xy_to_grid(closeBlueMonumentsCoordinates[0][0],closeBlueMonumentsCoordinates[0][1],inital_data))} grids away @{convert_xy_to_grid(closeBlueMonumentsCoordinates[0][0],closeBlueMonumentsCoordinates[0][1],inital_data)}, {closeBlueMonuments[1]['name']} {grids_apart(convert_xy_to_grid(sender_x,sender_y, inital_data),convert_xy_to_grid(closeBlueMonumentsCoordinates[1][0],closeBlueMonumentsCoordinates[1][1],inital_data))} grids away @{convert_xy_to_grid(closeBlueMonumentsCoordinates[1][0],closeBlueMonumentsCoordinates[1][1],inital_data)}, {closeBlueMonuments[2]['name']} {grids_apart(convert_xy_to_grid(sender_x,sender_y, inital_data),convert_xy_to_grid(closeBlueMonumentsCoordinates[2][0],closeBlueMonumentsCoordinates[2][1],inital_data))} grids away @{convert_xy_to_grid(closeBlueMonumentsCoordinates[2][0],closeBlueMonumentsCoordinates[2][1],inital_data)}")

    #red
    @Command(server_details)
    async def red(command: ChatCommand):
        team_info = await socket.get_team_info()
        for member in team_info.members:
            if member.steam_id == command.sender_steam_id:
                sender_x = member.x
                sender_y = member.y
                break
        closeRedMonuments, closeRedMonumentsCoordinates = closest_red_monuments(sender_x,sender_y,map.monuments)
        await socket.send_team_message(f"The closest places to get a red card are, {closeRedMonuments[0]['name']} {grids_apart(convert_xy_to_grid(sender_x,sender_y, inital_data),convert_xy_to_grid(closeRedMonumentsCoordinates[0][0],closeRedMonumentsCoordinates[0][1],inital_data))} grids away @{convert_xy_to_grid(closeRedMonumentsCoordinates[0][0],closeRedMonumentsCoordinates[0][1],inital_data)}, {closeRedMonuments[1]['name']} {grids_apart(convert_xy_to_grid(sender_x,sender_y, inital_data),convert_xy_to_grid(closeRedMonumentsCoordinates[1][0],closeRedMonumentsCoordinates[1][1],inital_data))} grids away @{convert_xy_to_grid(closeRedMonumentsCoordinates[1][0],closeRedMonumentsCoordinates[1][1],inital_data)}, {closeRedMonuments[2]['name']} {grids_apart(convert_xy_to_grid(sender_x,sender_y, inital_data),convert_xy_to_grid(closeRedMonumentsCoordinates[2][0],closeRedMonumentsCoordinates[2][1],inital_data))} grids away @{convert_xy_to_grid(closeRedMonumentsCoordinates[2][0],closeRedMonumentsCoordinates[2][1],inital_data)}")
            
            

    #hi
    @Command(server_details,aliases=["hello", "hey", "HI", "Hi", "hI"])
    async def hi(command : ChatCommand):
        if not verify_name(command.sender_name):
            await socket.send_team_message(f"Hi, unknown team member.")
        else:
            await socket.send_team_message(f"Hi, {command.sender_name}.")
    
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
        for member in team_info.members:
            if len(message) > 110:
                await socket.send_team_message(message)
                message = ""

            if not verify_name(member.name):
                name = 'unknown team member'
            else:
                name = member.name
            
            if not member.is_online:
                offlineMembers += name
                offlineMembers += f"{Emoji.HEART}"
            elif member.is_alive:
                if closest_monument(member.x,member.y,map.monuments) == None:
                    message += f'{name}: ALIVE @{convert_xy_to_grid(member.x, member.y, inital_data)}\n'
                    message+=f'{Emoji.HEART}'
                else:
                    message += f'{name}: ALIVE @{monuments_readable[closest_monument(member.x,member.y,map.monuments)]["name"]} {convert_xy_to_grid(member.x, member.y, inital_data)}\n'
                    message+=f'{Emoji.HEART}'
            else:
                days, hours, minutes = convert_epoch_to_hours(member.death_time)
                message += f'{name}: DEAD @{convert_xy_to_grid(member.x,member.y,inital_data)} near {closest_monument(member.x,member.y,map.monuments)} {minutes} min ago\n'
                message+=f'{Emoji.SKULL}'
            
        await socket.send_team_message(message)
        if offlineMembers == "":
            pass
        else:
            await socket.send_team_message(f'Offline Members: {offlineMembers}')

    

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
    async def watchForDeaths():
        reported_deaths = set()
        while True:
            team_info = await socket.get_team_info()
            for member in team_info.members:
                if member.is_alive:
                    reported_deaths.discard(member.steam_id)
                    continue
                if member.steam_id not in reported_deaths:
                    reported_deaths.add(member.steam_id)
                    name = 'unknown team member' if not verify_name(member.name) else member.name
                    if closest_monument(member.x,member.y,map.monuments) == None:
                        await socket.send_team_message(f'{name} is dead @{convert_xy_to_grid(member.x, member.y, inital_data)}')
                    else:
                        await socket.send_team_message(f'{name} is dead @{monuments_readable[closest_monument(member.x,member.y,map.monuments)]["name"]} {convert_xy_to_grid(member.x, member.y, inital_data)}')
            await asyncio.sleep(3)

    asyncio.create_task(watchForDeaths())
       

    async def watchForCargoHeli(): #fix corner calcluation + add what direction cargo is going in.
        reported_sightings = set()
        while True:
            event_info = await socket.get_markers()
            for event in event_info:
                if event.type in (5, 8): 
                    if event.type not in reported_sightings:
                        await socket.send_team_message(f'{event_ids[event.type]} is coming in from {whatCorner(event.x,event.y,inital_data)} {convert_xy_to_grid(event.x,event.y,inital_data)}.')
                        reported_sightings.add(event.type)
                else:
                    reported_sightings.discard(event.type)
            await asyncio.sleep(5)

    asyncio.create_task(watchForCargoHeli())

    












    
    await socket.hang()
    await socket.disconnect()

asyncio.run(main())
