'''
Collection of helpful functions/methods
'''

# local
from config.config import *

def deconstruct_arrivals(arrivals):
    # Example usage
    print(arrivals)

    cleaned = []
    for arrival in arrivals:
        cleaned.append(f"D: {arrival['orig_departure_time']} | A: {arrival['orig_arrival_time']} | S: {arrival['orig_delay']}")
    return cleaned