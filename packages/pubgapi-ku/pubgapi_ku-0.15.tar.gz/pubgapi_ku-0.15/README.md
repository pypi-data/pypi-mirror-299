# PUBG API Wrapper for Pandas
This package is under development; thus, some features may not work correctly or exist.

## Installation
You can install this module using pip (pip3)
```bash
pip install pubgapi-ku
```

## Components
### Modules
#### 1. API Connector
The module contains <b>Connector</b> class which has functions to get raw JSON data using <i>PUBG API</i> provided by <i>PUBG Developer Portal</i> (https://developer.pubg.com/).
All data which can be collected using this module can also be collected by the <b>DataWrapper</b> class, which provides data as <i>Pandas DataFrame</i> type using <b>Connector</b> class internally.
Therefore, there is no need to necessarily use <b>API Connector</b> module and <b>Connector</b> class in most cases.

##### Usage
To use <b>Connector</b> class, you must generate a <i>PUBG API key</i>. Refer instruction of <i>PUBG Developer Portal</i> (https://documentation.pubg.com/en/getting-started.html)
```Python
from pubgapiku import api_connector

conn = Connector(<your_api_key>)
sample_matches = conn.sample_matches()
```
##### Functions
- <img src='./docs/images/fn_sample_matches.png' height=32px align=center></img>
Return a dictionary(dict)-type containing a list of sample matches within 24 hours in UTC
When the API request was not successful (the response code was not 200), the function returns <i>None</i>

- <img src='./docs/images/fn_players.png' height=32px align=center></img>
Return a dictionary-type value containing players information
When the API request was not successful (the response code was not 200), the function returns <i>None</i>
    - Keyword arguments
        - <code><b>ids:list[str]</b></code> Filters by player IDs
        - <code><b>names:list[str]</b></code> Filters by player names

- <img src='./docs/images/fn_matches.png' height=32px align=center></img>
Return a dictionary-type value containing a match's information
When the API request was not successful (the response code was not 200), the function returns <i>None</i>
    - Argument
        - <code><b>match_id:str</b></code> The ID of the match for which you want to collect information

- <img src='./docs/images/fn_telemetry_addr.png' height=32px align=center></img>
Return the address of telemetry data of a match from the match's data
When the address of telemetry data was not found, the function return <i>None</i>
    - Argument
        - <code><b>match_data:dict</b></code> A match data which is obtained from <i>match</i> function

- <img src='./docs/images/fn_get_telemetry.png' height=32px align=center></img>
Return a dictionary-type value containing a match's telemetry data of the target match
When the request was not successful (the response code was not 200), the function returns <i>None</i>
    - Argument
        - <code><b>addr:str</b></code> The address of the target telemetry data obtained from <i>telemetry_addr</i> function

#### 2. Data Wrapper
The module contains <b>DataWrapper</b> class, which has functions to get PUBG data from <i>PUBG API</i> as <i>Pandas DataFrame</i> data type
Since <b>DataWrapper</b> class works based on <b>Collector</b> class, a PUBG API key is also needed to use <b>DataWrapper</b> class

##### Usage
##### Functions