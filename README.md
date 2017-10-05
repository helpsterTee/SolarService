# SolarService
Parses planetary Kp index from NOAA and sends warning via Pushover when geomagnetic storms happen

## Prequisites
- Python3
```python
pip install python-pushover
```
- register with [Pushover](https://pushover.net) and create an application key there
- fill in settings.json with your Pushover user token and api key
- run in endless loop
