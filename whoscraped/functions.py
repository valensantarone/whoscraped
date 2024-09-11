from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from bs4 import BeautifulSoup
from .exceptions import CantGetMatchData
import pandas as pd
import json
import re
from contextlib import contextmanager

@contextmanager
def browser_context():
    """Context manager for handling the browser lifecycle."""
    browser = init_browser()
    try:
        yield browser
    finally:
        browser.quit()

def init_browser():
    """Initialize a new browser session."""
    return webdriver.Chrome()

def get_match_data(match_url):
    """Get match information from a WhoScored data centre match.

    Args:
        match_url (str): Full link from a WhoScored data centre match.

    Returns:
        dict: Data of the match in JSON format.

    Raises:
        CantGetMatchData: If the required data is not found in the page source.
    """
    if match_url.split('/')[5] != 'Live':
        raise CantGetMatchData
    
    with browser_context() as browser:
        try:
            browser.get(match_url)
            source = browser.page_source
            soup = BeautifulSoup(source, 'html.parser')
            
            soup_str = str(soup)
            pattern = re.compile(r'require\.config\.params\["args"\] = ({.*?});', re.DOTALL)
            match = pattern.search(soup_str)

            if match and 'matchCentreData' in match.group(1):
                js_object = match.group(1)
            else:
                raise CantGetMatchData("Match data not found.")
            
            # Add quotes to the keys
            object_splitted = js_object.split('\n')
            for i in range(len(object_splitted[1:-1])):
                key = object_splitted[i+1].replace(' ', '').split(':')[0]
                js_object = re.sub(key, f'"{key}"', js_object)
            
            # Load the JSON object
            data = json.loads(js_object)
            return data
        except (NoSuchWindowException, WebDriverException):
            raise CantGetMatchData("Could not access the browser window.")

def get_match_passes(match_url):
    """Get all passes from both teams in a match.

    Args:
        match_url (str): Full link from a WhoScored data centre match.
    
    Returns:
        pd.DataFrame: DataFrame containing all pass event information.
    """
    data = get_match_data(match_url)

    # Collect rows in a list before creating DataFrame for performance
    rows = []

    for event in data['matchCentreData']['events']:
        if event.get('type', {}).get('displayName') == 'Pass':
            row_data = {
                'minute': event.get('minute', 0),
                'second': event.get('second', 0),
                'half': event.get('period', {}).get('displayName', 'Unknown'),
                'teamId': event.get('teamId', None),
                'playerId': event.get('playerId', None),
                'playerName': data['matchCentreData']['playerIdNameDictionary'].get(str(event['playerId']), 'Unknown'),
                'x': event.get('x', 0.0),
                'y': event.get('y', 0.0),
                'endX': event.get('endX', 0.0),
                'endY': event.get('endY', 0.0),
                'outcome': event.get('outcomeType', {}).get('displayName', 'Unknown'),
                'isTouch': event.get('isTouch', False)
            }
            rows.append(row_data)

    # Create DataFrame from list of rows
    df = pd.DataFrame(rows)
    return df
