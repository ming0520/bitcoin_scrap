import requests
# Importing the logging module
import logging
import sys


# Setting the basic configuration for logging, such as the level, the format and the file name
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='C:\\Other Project\\Ads\\Bitcoin Scraping\\example.log')

# Creating a logger object
logger = logging.getLogger()

server_url = 'http://127.0.0.1:8000'
api_url = f'{server_url}/scrap/api'

# Check if the script is being run with the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python my_script.py <argument>")
    sys.exit(1)

# Get the argument provided
argument = sys.argv[1]

def save_daily():
    return(f'{api_url}/bitstamp/save_daily')

def save_hourly():
    return (f'{api_url}/bitstamp/save_hourly')

def save_minutely():
    return (f'{api_url}/bitstamp/save_minutely')

def scrap_today():
    return(f'{server_url}/scrap/scrap_today')

def switch_case(argument):
    switcher = {
        'save_daily': save_daily,
        'save_hourly': save_hourly,
        'save_minutely': save_minutely,
        'scrap_today': scrap_today,
    }
    # Get the function corresponding to the argument and execute it
    func = switcher.get(argument, lambda: "Invalid function")
    return func()

try:
    result = switch_case(argument)
    response = requests.get(result)
    logger.info(f'switch_case: {argument}, response: {response.status_code} ,result: {response.text}')
except Exception as e:
    logger.error(f'save_daily: Error while saving daily data: {e}')


for handler in logger.handlers:
    handler.close()
    logger.removeHandler(handler)