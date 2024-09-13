# WhoScraped

Library for scraping football data from [WhoScored](https://www.whoscored.com/) matches.

## Installation

To install this library, use:

```bash
pip install whoscraped
```

To upgrade the library, use:

```bash
pip install --upgrade whoscraped
```

## Prerequisites
1. Python 3.6 or higher
2. Google Chrome browser
3. Chromedriver installed and added to your system's PATH

## How to Use It
The library provides the following functions:

1. Get data from the match URL in JSON format:

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
match_data = whoscraped.get_match_data(match_url)
```

This function retrieves match data from the specified URL. The data is returned as a Python dictionary in JSON format.

2. Get all passes from both teams from a match URL or match json data:

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
passes_df = whoscraped.get_match_passes(match_url)
```

or

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
data = whoscraped.get_match_data(url)
passes_df = whoscraped.get_match_passes(data)
```

This function gets all pass events from the specified match URL or json object with match data and returns a Pandas DataFrame containing the pass information.

3. Get all stats from both teams from a match URL or match json data:

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
stats_df = whoscraped.get_team_stats(match_url)
```

or

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
data = whoscraped.get_match_data(url)
stats_df = whoscraped.get_team_stats(data)
```

This function gets all the home and away team stats from the specified match URL or json object with match data and returns a Pandas DataFrame containing the information.

4. Get shotmap of a match from its URL or json data:

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
shots_df = whoscraped.get_shotmap(match_url)
```

or

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
data = whoscraped.get_match_data(url)
shots_df = whoscraped.get_shotmap(data)
```

This function gets all the shots from a match and returns a Pandas DataFrame containing the information.

5. Get players stats of a match from its URL or json data:

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
stats_df = whoscraped.get_players_stats(match_url)
```

or

```python
import whoscraped

match_url = "https://www.whoscored.com/Matches/1699239/Live/International-FIFA-World-Cup-2022-Argentina-France"
data = whoscraped.get_match_data(url)
stats_df = whoscraped.get_players_stats(data)
```

This function gets all the players individual stats from both teams and returns a Pandas DataFrame containing the information.

## Handling Errors
If you encounter an error, such as CantGetMatchData, ensure that the match URL is correct and that the WhoScored page has the necessary data.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request. Ensure that your code passes all tests and adheres to the project's coding standards.