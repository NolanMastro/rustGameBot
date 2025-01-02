import asyncio
import time
import datetime
from PIL import Image
from rustplus import RustSocket, CommandOptions, Command, ServerDetails, ChatCommand, EntityEventPayload, TeamEventPayload, ChatEventPayload, ProtobufEvent, ChatEvent, EntityEvent, TeamEvent, Emoji

#send location of dead teamates
#/turrets to turn on all turrets.
#/blue_card shows nearby location to get blue card.
#/red_card shows nearby location to get red card.


#




async def main():
    info ={}


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
    
    #print(convert_xy_to_grid(team_info.members[1].x,team_info.members[1].y, inital_data))
        




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
                message += f'{name}: DEAD @{team_info.members[i].death}\n'
                message+=f'{Emoji.SKULL}'
            
        await socket.send_team_message(message)
        await socket.send_team_message(f'Offline Members: {offlineMembers}')


    @Command(server_details)
    async def events(command: ChatCommand):
        markers = await socket.get_markers()
        for marker in markers:
            #if marker.type in (1,3,7):
                #continue
            #else:
            print(f'{types[marker.type]}, type {marker.type} detected at {convert_xy_to_grid(marker.x,marker.y,inital_data)}')

    def convert_epoch_to_hours(epoch_timestamp):
        current_time = datetime.datetime.now()
        target_time = datetime.datetime.fromtimestamp(epoch_timestamp)
        time_difference = target_time - current_time

        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        return days, hours, minutes
        
        


    @Command(server_details)
    async def tc(command: ChatCommand):
        team_chat = await socket.get_team_chat()
        latest_message = team_chat[-1].message if team_chat else ""
        
        if latest_message.startswith("!tc"):
            try:
                _, number = latest_message.split(maxsplit=1)
                entity_id = int(number)
                print(f'trying socket with num {number}')
                tc_info = await socket.get_entity_info(entity_id)
                print(f'type: {tc_info.type}')
                print(f'value{tc_info.value}')
                print(f'capacity: {tc_info.capacity}')
                print(f'has_protection: {tc_info.has_protection}')
                days, hours, minutes = convert_epoch_to_hours(tc_info.protection_expiry)
                print(f'epoch {tc_info.protection_expiry}')
                print(f'until decay: {days} days, {hours} hours, {minutes} min')
                
            
            except ValueError:
                print("Invalid command format. Use: !tc <number>")
        else:
            print("No valid command detected.")
        
        
        

                

    
    
        
        
    
    









    
    await socket.hang()
    await socket.disconnect()

asyncio.run(main())
