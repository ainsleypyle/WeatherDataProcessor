# WeatherDataProcessor
Description:

The Weather Station Data Processor is a Python application designed to process weather data coming from different weather stations. It handles incoming events such as weather samples (temperature readings) and control commands (like "snapshot" and "reset"). The program processes this data in real-time, storing the highest and lowest temperatures for each station and providing a snapshot of the latest data when requested. Additionally, it supports resetting the stored data to clear out all accumulated information.

The project is made up of two key components:

weather.py - The main processing logic for handling events and storing the station data.

test_weather.py - Unit tests to verify the correctness of the logic in weather.py.

Features:

Sample Events: The program processes incoming weather data samples (temperature readings) and updates the highest and lowest temperature for each station.

Snapshot Command: The "snapshot" command generates a snapshot of the current highest and lowest temperatures for each station, along with a timestamp.

Reset Command: The "reset" command clears all stored station data and resets the tracking of temperatures.

Real-Time Processing: The program handles streams of events and maintains up-to-date records of the temperature data as new events come in.

