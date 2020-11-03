import requests
import json
import time
import threading
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from config import MTA_API_KEY, MTA_URL, PERIOD

class DelayTracker():
    def __init__(self):
        self.feed = gtfs_realtime_pb2.FeedMessage()
        self.trains = {}
        self.start_time = time.time()
        self.currently_delayed = set()
        self.thread = threading.Thread(target=self.update_loop, args=(), daemon=True)
        self.mutex = threading.Lock()

    def start(self):
        self.thread.start()

    def uptime(self, line):
        self.mutex.acquire()
        if line.upper() in self.trains:
            total_time = time.time() - self.start_time
            prev_delayed = self.trains[line]['total_time_delayed']
            curr_delayed = time.time() - self.trains[line]['delayed_since'] if self.trains[line]['delayed_since'] else 0
            self.mutex.release()
            return (1 - ((prev_delayed + curr_delayed)/ total_time))
        else:
            self.trains[line] = {
                'id': line.upper(),
                'delayed_since': None,
                'total_time_delayed': 0
            }
            self.mutex.release()
            return 1.0

    def status(self, line):
        self.mutex.acquire()
        output = line.upper() in self.currently_delayed
        self.mutex.release()
        return output

    def update(self):
        res = requests.get(MTA_URL, headers={'x-api-key': MTA_API_KEY})
        self.feed.ParseFromString(res.content)
        delays = self.filter_feed_for_delays()

        self.mutex.acquire()
        #if something is in delays but not in currently_delayed, add to currently_delayed, and update train times
        new_delays = delays - self.currently_delayed
        for delayed_line in new_delays:
            print("Line {} is experiencing delays".format(delayed_line))
            if delayed_line in self.trains:
                self.trains[delayed_line]['delayed_since'] = time.time()
            else:
                self.trains[delayed_line] = {
                    'id': delayed_line,
                    'delayed_since': time.time(),
                    'total_time_delayed': 0
                }

        #if something is in currently_delayed, but not in delays, remove, and update train times
        old_delays = self.currently_delayed - delays
        for delayed_line in old_delays:
            print("Line {} is now recovered".format(delayed_line))
            self.trains[delayed_line]['total_time_delayed'] += time.time() - self.trains[delayed_line]['delayed_since']
            self.trains[delayed_line]['delayed_since'] = None

        self.currently_delayed = delays
        self.mutex.release()

    def update_loop(self):
        while(True):
            self.update()
            time.sleep(PERIOD)

    def filter_feed_for_delays(self):
        output = set()
        for feed_entity in self.feed.entity:
            #converts feed entity to dictionary
            entity = MessageToDict(feed_entity)
            #attempts to get status from entity
            status = entity.get('alert') and \
                    entity['alert'].get('headerText') and \
                    entity['alert']['headerText'].get('translation') and \
                    entity['alert']['headerText']['translation'][0].get('text')
            #if the status is delays, attempt to grab the affected routes (trains)
            if status == "Delays" and 'informedEntity' in entity['alert']:
                for informedEntity in entity['alert']['informedEntity']:
                    if 'routeId' in informedEntity:
                        output.add(informedEntity['routeId'])
        return output
