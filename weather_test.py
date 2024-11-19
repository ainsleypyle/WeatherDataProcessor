#
# Created on Sat Nov 02 2024
# Unit tests to verify the correct outputs for process_events().
# Ainsley Pyle
#
from . import weather

#Test function for a single weather sample.
def test_single_sample():
    events = [
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1}
    ]
    results = list(weather.process_events(events))
    assert not results  #No output for sample messages.

#Test function for snapshot command.
def test_snapshot():
    events = [
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "control", "command": "snapshot"}
    ]
    results = list(weather.process_events(events))
    assert results == [{
        "type": "snapshot",
        "asOf": 1672531200000,
        "stations": {"Foster Weather Station": {"high": 37.1, "low": 37.1}}
    }] #Output should be most recent sample.

#Test function for multiple samples and snapshot command.
def test_multiple_samples():
    events = [
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531201000, "temperature": 32.5},
        {"type": "control", "command": "snapshot"}
    ]
    results = list(weather.process_events(events))
    assert results == [{
        "type": "snapshot",
        "asOf": 1672531201000,
        "stations": {"Foster Weather Station": {"high": 37.1, "low": 32.5}}
    }] #Output should have updated high and low values.

#Test function for multiple samples and weather stations followed by and snapshot command.
def test_multiple_samples_and_stations():
    events = [
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531201000, "temperature": 39.0},
        {"type": "sample", "stationName": "Montrose Beach",
         "timestamp": 1672531202000, "temperature": 36.5},
        {"type": "sample", "stationName": "Montrose Beach",
         "timestamp": 1672531203000, "temperature": 38.2},
        {"type": "control", "command": "snapshot"}
    ]
    results = list(weather.process_events(events))
    assert results == [{
        "type": "snapshot",
        "asOf": 1672531203000,
        "stations": {"Foster Weather Station": {"high": 39.0, "low": 37.1}, 
                     "Montrose Beach": {"high": 38.2, "low": 36.5}} 
    }] #Output should have updated high and low values.

#Test function that tests no data is returned with reset command.
def test_reset():
    events = [
        {"type": "sample", "stationName": "Foster Weather Station",
         "timestamp": 1672531200000, "temperature": 37.1},
        {"type": "control", "command": "reset"}
    ]
    results = list(weather.process_events(events))
    assert results == [{
        "type": "reset",
        "asOf": 1672531200000
    }]

    #Now check that a snapshot returns no data.
    results = list(weather.process_events([{"type": "control", "command": "snapshot"}]))
    assert not results
