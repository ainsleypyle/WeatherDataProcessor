#
# Created on Sat Nov 02 2024
#
# Ainsley Pyle
#
from typing import Any, Iterable, Generator
from collections import defaultdict

class UnknownMessageTypeError(Exception):
    pass

def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:

    #Object initialization.
    station_data = defaultdict(lambda: {"high": float('-inf'), "low": float('inf')})
    last_timestamp = None

    #Looping through the events from STDIN.
    for line in events:
        event_type=line.get("type")

        #Scenario when type="Sample".
        if event_type=="sample":
            station_name=line["stationName"]
            temperature=line["temperature"]
            timestamp=line["timestamp"]
            #Updating the station high and low data as it comes in through the stream.
            station_data[station_name]["high"] =max(station_data[station_name]["high"], temperature)
            station_data[station_name]["low"] = min(station_data[station_name]["low"], temperature)
            last_timestamp = timestamp

        #Scenario when type="Control".
        elif event_type=="control":
            command=line["command"]

            #If control is type snapshot, most updated data is sent to STDOUT.
            if command=="snapshot":
                if last_timestamp is not None:
                    yield{
                        "type":"snapshot",
                        "asOf": last_timestamp,
                        "stations": {name: {"high": data["high"], "low": data["low"]} 
                                     for name, data in station_data.items()}
                    }
            #If control is type reset, clear the data.
            elif command=="reset":
                #Clearing station_data as a result of the reset command.
                station_data.clear()

                yield{
                    "type":"reset",
                    "asOf": last_timestamp
                }
                #Setting last_timestamp to none so that any further snapshot messages are ignored.
                last_timestamp=None
            else:
                raise UnknownMessageTypeError("Please verify input.")
        else:
            raise UnknownMessageTypeError("Please verify input.")
        