import datetime

monuments_readable = {
    "ferryterminal": {"name": "Ferry Terminal", "card": None},
    "train_tunnel_display_name": {"name": "Train Tunnels", "card": None},
    "harbor_2_display_name": {"name": "Harbor", "card": "Blue"},
    "harbor_display_name": {"name": "Harbor", "card": "Blue"},
    "fishing_village_display_name": {"name": "Fishing Village", "card": None},
    "large_fishing_village_display_name": {"name": "Large Fishing Village", "card": None},
    "AbandonedMilitaryBase": {"name": "Abandoned Military Base", "card": None},
    "arctic_base_a": {"name": "Arctic Base", "card": "Red"},
    "launchsite": {"name": "Launch Site", "card": None},
    "train_yard_display_name": {"name": "Trainyard", "card": "Red"},
    "military_tunnels_display_name": {"name": "Minitary Tunnels", "card": None},
    "excavator": {"name": "Excavator", "card": None},
    "outpost": {"name": "Outpost", "card": "Blue"},
    "missile_silo_monument": {"name": "Missile Silo", "card": "Red"},
    "junkyard_display_name": {"name": "Junkyard", "card": None},
    "stables_a": {"name": "Ranch", "card": None},
    "airfield_display_name": {"name": "Airfield", "card": "Red"},
    "water_treatment_plant_display_name": {"name": "Water Treatment", "card": "Red"},
    "power_plant_display_name": {"name": "Power Plant", "card": "Red"},
    "sewer_display_name": {"name": "Sewer Branch", "card": "Blue"},
    "satellite_dish_display_name": {"name": "Satellite Dish", "card": "Blue"},
    "mining_quarry_hqm_display_name": {"name": "HQM Quarry", "card": None},
    "mining_quarry_stone_display_name": {"name": "Stone Quarry", "card": None},
    "mining_quarry_sulfur_display_name": {"name": "Sulfer Quarry", "card": None},
    "dome_monument_name": {"name": "Dome", "card": None},
    "stables_b": {"name": "Barn", "card": None},
    "train_tunnel_link_display_name": {"name": "Train Tunnels", "card": None},
    "mining_outpost_display_name": {"name": "Mining Outpost", "card": None},
    "radtown": {"name": "Radtown", "card": None},
    "gas_station": {"name": "Gas Station", "card": None},
    "supermarket": {"name": "Supermarket", "card": None},
    "underwater_lab": {"name": "Underwater Labs", "card": None},
    "DungeonBase": {"name": "Dungeon Base", "card": None},
    "oil_rig_small": {"name": "Small Oil", "card": None},
    "large_oil_rig": {"name": "Large Oil", "card": None},
    "swamp_c": {"name": "Swamp", "card": None},
    "lighthouse_display_name": {"name": "Lighthouse", "card": None},
    "bandit_camp": {"name": "Bandit", "card": None}
    
    }
event_ids = {
    1: "Player",
    2: "Explosion",
    3: "VendingMachine",
    4: "CH47",
    5: "Cargo",
    6: "Crate",
    7: "GenericRadius",
    8: "Attack Heli"
}


def grids_apart(grid1, grid2):

    def parse_grid(grid):
        letter = ''.join([c for c in grid if c.isalpha()])
        number = int(''.join([c for c in grid if c.isdigit()]))
        return letter, number
    
    def letter_to_index(letter):
        index = 0
        for i, char in enumerate(reversed(letter)):
            index += (ord(char.upper()) - ord('A')) * (26 ** i)
        return index
    
    letter1, number1 = parse_grid(grid1)
    letter2, number2 = parse_grid(grid2)
    
 
    letter1_index = letter_to_index(letter1)
    letter2_index = letter_to_index(letter2)

    letter_diff = abs(letter1_index - letter2_index)
    number_diff = abs(number1 - number2)
    
    return letter_diff + number_diff

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


def whatCorner(x, y, initdata):
    trueSize = initdata.size
    
    mid_x = trueSize / 2
    mid_y = trueSize / 2

    if x < mid_x and y < mid_y:
        return "Top Left"
    elif x >= mid_x and y < mid_y:
        return "Top Right"
    elif x < mid_x and y >= mid_y:
        return "Bottom Left"
    else:
        return "Bottom Right"


def verify_name(name):
    for char in name:
        if not (char.isalpha() or char.isdigit() or char == " "):
            return False
    return True
    
def convert_epoch_to_hours(epoch_timestamp):
    current_time = datetime.datetime.now()
    target_time = datetime.datetime.fromtimestamp(epoch_timestamp)
    time_difference = target_time - current_time

    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return days, hours, minutes


def closest_monument(x, y, monuments): #returns a monument name only if player is within bounds.
        for monument in monuments:
            distance_x = abs(x - monument.x)
            distance_y = abs(y - monument.y)
            
            if distance_x <= 100 and distance_y <= 100:
                return monument.token
        
        return None


def closest_blue_monuments(x, y, monuments): #returns a list of blue card only, sorted by distance monuments

    sortedByDistanceMonuments = sorted(
        monuments,
        key=lambda monument: ((x - monument.x) ** 2 + (y - monument.y) ** 2) ** 0.5
    )

    blueMonumentsSorted = []
    blueMonumentsLocation = []
    for monument in sortedByDistanceMonuments:
        if monuments_readable[monument.token]['card'] == 'Blue':
             blueMonumentsSorted.append(monuments_readable[monument.token])
             blueMonumentsLocation.append((monument.x,monument.y))
    return blueMonumentsSorted, blueMonumentsLocation

    
def closest_red_monuments(x, y, monuments): #returns a list of red card only, sorted by distance monuments

    sortedByDistanceMonuments = sorted(
        monuments,
        key=lambda monument: ((x - monument.x) ** 2 + (y - monument.y) ** 2) ** 0.5
    )

    redMonumentsSorted = []
    redMonumentsLocation = []
    for monument in sortedByDistanceMonuments:
        if monuments_readable[monument.token]['card'] == 'Red':
            redMonumentsSorted.append(monuments_readable[monument.token])
            redMonumentsLocation.append((monument.x,monument.y))
    return redMonumentsSorted, redMonumentsLocation
