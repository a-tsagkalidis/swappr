# <span style="color: #e8b600">Swappr</span>
**Author**: Argyrios Tsagkalidis

**Location**: Thessaloniki, Greece

**License**: MIT

**Video Demo**:  <URL HERE>

## <span style="color: #e8b600">Description</span>
Swappr is a web app project that helps the users to swap their rented houses.

The users create an account, uploads their rented house's specifications, and explore potential matches for a hassle-free swap experience.

The app uses an intelligent algorithm that suggests compatible house swap options, ensuring that the user's preferences align with potential matches. The algorithm uses a matching score based on house characteristics, house location, and desired move destination.

## <span style="color: #e8b600">Running the app</span>
Swappr repo comes with no **.db** or **.log** files. These necessities will be created on program initialization. To initiate swappr run:
```sh
python app.py
```
But before you run the program for the first time, make sure that you have created a virtual environment and have installed all Python dependencies.

### <span style="color: #c9b7a4">Create a virtual environment</span>
Before you run Swappr it is recommended to create a virtual environment where all Python dependencies will be installed.
While in working directory run:
```sh
python -m venv .venv
```
Notice that a `.venv` folder has been created.

### <span style="color: #c9b7a4">Install Python dependencies</span>
After your venv creation, you should install all swappr Python dependencies. While in working directory run:
```sh
pip install -r requirements.txt
``` 

### <span style="color: #c9b7a4">Argument parser</span>
Swappr comes with an embedded argument parser and developers can check its options using `python app.py -h`. Optinal arguments are:

- `-d` or `--debug` enables Flask's embedded debug mode for testing purposes
- `-b` or `--backup` runs automated backup routines for the database and log files
- `-l` or `--limiter` enables a request limiter to protect the backend from spam
- `-p` or `--premademockups` inserts a premade JSON of mockup users and submitted houses into the database. The premade mockups are tailored in such way so that developers can test the matching algorithm for every probable **location/desired move location** scenario
- `-m INTEGER INTEGER` or `--mockupsgen INTEGER INTEGER` creates mockup users and submitted houses to test the matching algorithm. First integer is the number of users to be created, while the second is the number of the submitted houses. Submitted houses can't exceed the number of the mockup users - if so the program will limit submitted houses equal to users. The higher the number of mockups created, the higher the chance of catching a matching house during the test. *Recommended 3000+ Mockups*


## <span style="color: #e8b600">Developing tools</span>
Swappr uses the following programming languages, frameworks, and dev tools:

- **Python3** and **Flask** mini framework package for the backend
- **HTML**/**CSS Bootstrap 5.2**/**JavaScript** for the frontend
- **Jinja2** for the HTML templates
- **AJAX** for asynchronous request logic
- **SQLite3** for the database handling
- **Bash** for backup functionalities
- **noUiSlider JavaScript** package to control input values for searching filters
- **jQuery.validate** package for extra frontend validation

## <span style="color: #e8b600">Backend</span>
Backend convention relies on splitted .py files (aka modules) where the proper code for every related section is contained. Python files are described as follows:

### <span style="color: #c9b7a4">app.py</span>
This is the main file where <b style="color: #eedebf">Swappr Initialization</b> and the <b style="color: #eedebf">Route Creation</b> for all sections take place.

#### <span style="color: #eedebf">Swappr Initialization</span>
When **app.py** initiates the following functionalities take action:
- Configures a logger using loguru library
- Checks for given arguments such as `--backup`, `--limiter`, and/or `--premademockups`/`--mockupsgen INTEGER INTEGER` to call the corresponding functions.
- Checks if SQL database is present or else it creates it with the proper schema in **swappr.db**
- Checks if `locations` table in **swappr.db** matches with all the data in `locations.json` file. If new locations are present in the JSON file, then they are imported as new entries in **swappr.db** `locations` table

#### <span style="color: #eedebf">Route Creation</span>
Most routes have their corresponding .py file where their dependent functions are present. For instance **/search** route calls some functions that are imported from **fsearch.py**, while **/signup** route draws functions from **fsignup.py**, and so on...

    
### <span style="color: #c9b7a4">argparser.py</span>
This module uses <span style="color: #68ba6a">argparse</span> Python package to create argument option instances. Added argument are stored in argparser variable, which is imported in whatever .py module is needed.

### <span style="color: #c9b7a4">faccount.py</span>
Contains functions needed in **/account** route. Functions are:
- password_reset_validation(oldpassword, new_password, confirm_new_password, hash). Checks password reset input validity
- update_username_validation(new_username, user_id). Checks password reset input validity
- delete_account_validation(delete_account_confirmation, email). Checks password reset input validity

### <span style="color: #c9b7a4">fhelpers.py</span>
Contains functions needed many routes. Functions are:
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`cursor_execute`** | (query, *args) | Dynamically executes SQLite3 queries | `create_database_tables` | None |
| **`cursor_fetch`** | (query, *args) | Dynamically fetches data SQLite3 database | `create_database_tables` | tuples_to_dict |
| **`tuples_to_dict`** | (keys_tuple, values_tuple) | Converts two tuples into one dictionary | `cursor_fetch` | None |
| **`strong_password`** | (password) | Checks if a password is strong enough | `signup_validation`<sup>1</sup> `password_reset_validation`<sup>2</sup> | None |
| **`email_exists`** | (email) | Checks if email already exists in the database | `signup_validation`<sup>1</sup> | None |
| **`username_exists`** | (username, *args) | Checks if username already exists in the database | `signup_validation`<sup>1</sup> `update_username_validation`<sup>2</sup> | None |

**Sources**: <sup>1</sup>fsignup.py, <sup>2</sup>faccount.py

- cursor_execute(query, *args). Dynamically executes SQLite3 queries
- cursor_fetch(query, *args). Dynamically fetches data SQLite3 database
- tuples_to_dict(keys_tuple, values_tuple). Converts two tuples into one dictionary
- strong_password(password). Checks if a password is strong enough
- email_exists(email). Checks if email already exists in the database
- username_exists(username, *args). Checks if username already exists in the database. Excludes current session username in case of updating to a new username
- get_list_of_values(json_data, column_name). Converts a json file into a list with values of the selected column
- check_submitted_location(submitted_value, valid_values, error_message). Checks submitted location validity
- login_required(f). Decorate routes to require login
- comma(integer). Formats an integer by placing commas between thousands
- whitespace(text). Formats a snakecase string into a readable title

### <span style="color: #c9b7a4">flog.py</span>
Contains functions needed for history logger. Functions are:
- log(message, level='INFO', indent=28). Dynamically handles log indentations and message level
- initialize_logger(). Initializes loguru history logger
- log_new_locations(locations_update, new_locations_flag). Add brief log info about newly inserted location entries in the database

### <span style="color: #c9b7a4">fsearch.py</span>
Contains the algorithmic functions and constant variables needed in **/search** route
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`room_tolerance_factor`**   | (tolerance, room) | Returns the tolerance factor that adjusts the maximum value of the criteria search ranges | `tolerance_factors` | None |
| **`tolerance_factors`** | (tolerance) | Returns varied multipliers that affect the criteria ranges to be used in the matching score algorithm | None | `room_tolerance_factor` |
| **`criteria_ranges`** | (primary_submission, TOLERANCE_FACTORS) | Returns varied ranges to be used in the calculation of the matching score for each search house result | None | None |
| **`validate_searched_digits`** | (square_meters, rental, bedrooms, bathrooms) | Validates digit-required and ranged-required fields| `search_validation` | None |
| **`validate_searched_location`** | (city, municipality, region) | Validates location input | `search_validation` | `check_submitted_location`<sup>1</sup> |
| **`search_validation`** | (exposure, house_type, square_meters, rental, bedrooms, bathrooms, city, municipality, region) | Validates input data | None | `validate_searched_digits` `validate_searched_location` |
| **`calculate_location_matching_score`** | (result, primary_submission) | Calculates and returns a location matching score | `location_matching` | None |
| **`location_matching`** | (primary_submission, search_results) | Iterates all search results and adds into them the calculated location matching score | None | `calculate_location_matching_score` |
| **`calculate_house_matching_score`** | (result, CRITERIA_RANGES) | Calculates and returns a house characteristics matching score | None | **`house_matching`** |
| **`house_matching`** | (search_results, CRITERIA_RANGES) | Iterates all search results and adds into them the calculated house characteristics matching score | None | `calculate_house_matching_score` |
| **`matching_summary`** | (search_results) | Iterates all search results and adds into them the summary matching score | None | None |

**Source:** <sup>1</sup>fhelpers.py


## Validation
Swappr uses validation logic for whatever input data the user's may send with their request. This validation takes place in frontend using html browser validation, jQuery.validate() methods, and custom JavaScript functions, while custom python functions are protecting the backend.
