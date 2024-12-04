'''
Program to send me texts / notify me of next trains and their status
'''

# external packages
import requests
from datetime import datetime

# local imports
from utils import email, septa, utils
from config.config import *

# entry point
if __name__ == "__main__":
    # initialize the SEPTA client
    septa_client = septa.SeptaAPIClient()
    sms_client = email.EmailSMSClient(EMAIL_ADDRESS, EMAIL_PASSWORD)

    last_sent_minute = None
    enable_loop = True

    print(f"> Loop: {'enabled' if enable_loop else 'disabled'} | Times: {NOTIF_TIMES if enable_loop else None} ")
    
    # testing, trigger on run
    if not enable_loop:
        if datetime.now().hour < 12:
            DEPARTURE_STATION = DEPARTURE_STATION_MORNING
            ARRIVAL_STATION = ARRIVAL_STATION_MORNING
        else:
            DEPARTURE_STATION = DEPARTURE_STATION_AFTERNOON
            ARRIVAL_STATION = ARRIVAL_STATION_AFTERNOON
        
        print(f"> Depart: {DEPARTURE_STATION} | Arrive: {ARRIVAL_STATION}")
        arrivals = septa_client.get_next_arrivals(
            DEPARTURE_STATION,
            ARRIVAL_STATION,
            num_results=3
        )
        with sms_client:
            utils.send_arrivals(arrivals, client=sms_client)

    # want this to run all day, erryday
    while enable_loop:
        #print(f"last sent: {last_sent_minute}")
        # retrieve relevant timestamp data
        curr_weekday, curr_hour, curr_minute, curr_second = utils.decompose_timestamp(datetime.now())

        if (curr_hour, curr_minute) in NOTIF_TIMES:
            if curr_minute != last_sent_minute:
                last_sent_minute = curr_minute

                if curr_hour < 12:
                    DEPARTURE_STATION = DEPARTURE_STATION_MORNING
                    ARRIVAL_STATION = ARRIVAL_STATION_MORNING
                else:
                    DEPARTURE_STATION = DEPARTURE_STATION_AFTERNOON
                    ARRIVAL_STATION = ARRIVAL_STATION_AFTERNOON
                
                print(f"> Depart: {DEPARTURE_STATION} | Arrive: {ARRIVAL_STATION}")

                arrivals = septa_client.get_next_arrivals(
                    DEPARTURE_STATION,
                    ARRIVAL_STATION,
                    num_results=3
                )
                with sms_client:
                    utils.send_arrivals(arrivals, client=sms_client)