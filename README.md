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
This module uses <span style="color: #68ba6a">argparse</span> Python library to create argument option instances. Added argument are stored in argparser variable, which is imported in whatever .py module is needed.

### <span style="color: #c9b7a4">faccount.py</span>
Contains functions needed in **/account** route. Functions are:
- password_reset_validation(oldpassword, new_password, confirm_new_password, hash). Checks password reset input validity
- update_username_validation(new_username, user_id). Checks password reset input validity
- delete_account_validation(delete_account_confirmation, email). Checks password reset input validity

### <span style="color: #c9b7a4">fhelpers.py</span>
Contains functions needed many routes. Functions are:
- cursor_execute(query, *args). Dynamically executes SQLite3 queries
- cursor_fetch(query, *args). Dynamically fetches data SQLite3 database
- tuples_to_dict(keys_tuple, values_tuple). Converts two tuples into one dictionary
- strong_password(password). Checks if a password is strong enough
- email_exists(email). Checks if email already exists in the database
- username_exists(username, *args). Checks if username already exists in the database. Excludes current session username in case of updating to a new username
- get_list_of_values(json_data, column_name). Converts a json file into a list with values of the selected column
- check_submitted_location(submitted_value, valid_values, error_message). Checks submitted location validity
## Validation
Swappr uses validation logic for whatever input data the user's may send with their request. This validation takes place in frontend using html browser validation, jQuery.validate() methods, and custom JavaScript functions, while custom python functions are protecting the backend.
- login_required(f). Decorate routes to require login
- comma(integer). Formats an integer by placing commas between thousands
- whitespace(text). Formats a snakecase string into a readable title