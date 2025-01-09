import datetime


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
    
def verify_name(name):  # string name
    for char in name:
        if not (char.isalpha() or char.isdigit()):
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


def closest_monument(x, y, monuments):
        for monument in monuments:
            distance_x = abs(x - monument.x)
            distance_y = abs(y - monument.y)
            
            if distance_x <= 100 and distance_y <= 100:
                return monument.token
        
        return None
