'''
Collection of helpful functions/methods
'''

# local
from utils import email
from config.config import *

def decompose_timestamp(now):
    '''
    Decompose the timestamp from datetime
    '''
    # weekday
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    curr_weekday = weekdays[now.weekday()]
    
    # hour, min, second
    curr_hour = now.hour
    curr_minute = now.minute
    curr_second = now.second
    
    #print(f"{curr_weekday} | {curr_hour} | {curr_minute} | {curr_second}")
    return curr_weekday, curr_hour, curr_minute, curr_second

def send_arrivals(arrivals, client):
    # Example usage
    message = ""
    for arrival in arrivals:
        message = message + "-" * 20
        message = message + f"\nDepart: {arrival['orig_departure_time']}\n"
        message = message + f"Arrive: {arrival['orig_arrival_time']}\n"
        message = message + f"Status: {arrival['orig_delay']}\n"
    
    message = message + "-" * 20


    # send message
    print(f"{message}")
    client.send(TO_ADDRESS, message)