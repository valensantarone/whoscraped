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
                raise CantGetMatchData
            
            # Add quotes to the keys
            object_splitted = js_object.split('\n')
            for i in range(len(object_splitted[1:-1])):
                key = object_splitted[i+1].replace(' ', '').split(':')[0]
                js_object = re.sub(key, f'"{key}"', js_object)
            
            # Load the JSON object
            data = json.loads(js_object)
            return data
        except (NoSuchWindowException, WebDriverException):
            raise CantGetMatchData

def get_match_passes(match_input):
    """Get all passes from both teams in a match.

    Args:
        match_input (str or dict): Either a full URL from a WhoScored data centre match (str) 
                                   or the match data in JSON format (dict).
    
    Returns:
        pd.DataFrame: DataFrame containing all pass event information.
    """
    if isinstance(match_input, str):
        data = get_match_data(match_input)
    elif isinstance(match_input, dict):
        if 'matchCentreData' not in match_input:
            raise CantGetMatchData
        else:
            data = match_input
    else:
        raise ValueError("The input must be a URL string or a JSON object.")

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

def get_team_stats(match_input):
    """Get a table with both team stats from a match, including the final score.
    
    Args:
        match_input (str or dict): Either a full URL from a WhoScored data centre match (str) 
                                   or the match data in JSON format (dict).
    
    Returns:
        pd.DataFrame: DataFrame containing all stats from home and away team (integer stats only).
    """
    
    if isinstance(match_input, str):
        data = get_match_data(match_input)
    elif isinstance(match_input, dict):
        if 'matchCentreData' not in match_input:
            raise CantGetMatchData
        else:
            data = match_input
    else:
        raise ValueError("The input must be a URL string or a JSON object.")
    
    def process_team_stats(team_data):
        skip_stats = ['minutesWithStats', 'ratings', 'possession', 'passSuccess', 'tackleSuccess', 'dribbleSuccess', 'aerialSuccess']
        
        team_rows = []
        for key, stats in team_data['stats'].items():
            if key not in skip_stats:
                total_stat = sum(stats.values())
                team_rows.append({key: int(total_stat)})
        return team_rows

    home_rows = process_team_stats(data['matchCentreData']['home'])
    away_rows = process_team_stats(data['matchCentreData']['away'])

    home_dict = {k: v for d in home_rows for k, v in d.items()}
    away_dict = {k: v for d in away_rows for k, v in d.items()}

    # Extract the score for home and away teams
    score_home, score_away = data['matchCentreData']['score'].split(' : ')
    
    # Add the score to the home and away dictionaries
    home_dict = {'score': int(score_home), **home_dict}
    away_dict = {'score': int(score_away), **away_dict}

    # Create the DataFrame
    df = pd.DataFrame([home_dict, away_dict], index=['home', 'away']).fillna(0).astype(int)
    
    return df

def get_shotmap(match_input):
    """Get a table with all the shots of the match.
    
    Args:
        match_input (str or dict): Either a full URL from a WhoScored data centre match (str) 
                                   or the match data in JSON format (dict).
    
    Returns:
        pd.DataFrame: DataFrame containing all shots information of the match.
    """
    
    if isinstance(match_input, str):
        data = get_match_data(match_input)
    elif isinstance(match_input, dict):
        if 'matchCentreData' not in match_input:
            raise CantGetMatchData
        else:
            data = match_input
    else:
        raise ValueError("The input must be a URL string or a JSON object.")
    
    rows = []
    for event in data['matchCentreData']['events']:
        if 'isShot' not in event:
            continue
        row = {
            'minute': event.get('minute'),
            'second': event.get('second'),
            'teamId': event.get('teamId'),
            'playerId': event.get('playerId'),
            'playerName': data['matchCentreData']['playerIdNameDictionary'][str(event.get('playerId'))],
            'x': event.get('x'),
            'y': event.get('y'),
            'period': event.get('period', {}).get('displayName'),
            'type': event.get('type', {}).get('displayName'),
            'blockedX': event.get('blockedX'),
            'blockedY': event.get('blockedY'),
            'goalMouthZ': event.get('goalMouthZ'),
            'goalMouthY': event.get('goalMouthY')
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    
    return df