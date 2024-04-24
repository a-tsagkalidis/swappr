# <span style="color: #e8b600">Swappr</span>
**Author**: Argyrios Tsagkalidis

**Location**: Thessaloniki, Greece

**License**: <a href="https://github.com/a-tsagkalidis/swappr/tree/main?tab=BSD-3-Clause-1-ov-file">BSD-3-Clause</a>

**Video Demo**: <a href="https://www.youtube.com/watch?v=SlrPxYH-5cI&ab_channel=ArgyriosTsagkalidis">CS50X Final Project - Swappr</a>

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
- `-m MOCKUPSGEN MOCKUPSGEN` or `--mockupsgen MOCKUPSGEN MOCKUPSGEN` creates mockup users and submitted houses to test the matching algorithm. First integer is the number of users to be created, while the second is the number of the submitted houses. Submitted houses can't exceed the number of the mockup users - if so the program will limit submitted houses equal to users. The higher the number of mockups created, the higher the chance of catching a matching house during the test. *Recommended 3000+ Mockups*


## <span style="color: #e8b600">Backup</span>
Running **app.py** with `-b` or `--backup` argument initiates a simple backup functionality by triggering **fbak.sh** file. Doing two directories are created if not already present. First is **bak.db** and the second is **bak.log**. In there **swappr.db** and **app.log** are backed up into subfolders named by datetime logic. Backup functionality is usable only once per minute.


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


## <span style="color: #e8b600">Frontend</span>
Frontend convention relies on HTML Jinja2 templates that are extensions of the prototype **layout.html** file, as well as in JavaScript functionalities from **script.js** file and CSS styling from **styles.css**.

Frontend also relies on the following list of well known JavaScript libraries:
- Bootstrap 5.2
- jQuery 3.7.1
- jQuery Validation v1.19.5
- Popper
- noUiSlider


## <span style="color: #e8b600">Backend</span>
Backend convention relies on splitted **.py** files (aka modules) where the proper code for every related section is contained. All modules and their functions are imported in a main module named as <span style="color: #68ba6a">**swapprfunctions**</span> which in turn is imported in **app.py**. For more information regarding backend functionality check section <b style="color: #eedebf">Custom modules</b>, but first you should read some information about **app.py** - the main file where Flask framework get initialized. 

### <span style="color: #c9b7a4">app.py</span>
This is the main file where <b style="color: #eedebf">Swappr Initialization</b> and the <b style="color: #eedebf">Route Creation</b> for all sections take place.

#### <span style="color: #eedebf">Swappr Initialization</span>
When **app.py** initiates the following functionalities take action:
- Configures a logger using loguru library
- Checks for given arguments such as `--backup`, `--limiter`, and/or `--premademockups`/`--mockupsgen MOCKUPSGEN MOCKUPSGEN` to call corresponding functions.
- Checks if SQL database is present or else it creates it with the proper schema in **swappr.db**
- Checks if **locations** table in **swappr.db** matches with all the data in **locations.json** file. If new locations are present in the JSON file, then they are imported as new entries in **swappr.db** **locations** table

#### <span style="color: #eedebf">Route Creation</span>
Most routes have their corresponding .py file where their dependent functions are present. For instance **/search** route calls some functions that are imported from **fsearch.py**, while **/signup** route draws functions from **fsignup.py**, and so on.


## <span style="color: #e8b600">Validation</span>
Swappr uses validation logic for whatever input data the user's may request. Validation takes place in frontend using browser's embedded validation, jQuery Validation Plugin methods, and custom JavaScript functions, while backend is being protected by custom Python functions.

Proper backend error handling prevents Swappr from crushes, where the errors are logged thanks to <span style="color: #68ba6a">**loguru**</span> Python package.


## <span style="color: #e8b600">Limiter</span>
Running **app.py** with `-l` or `--limiter` argument initiates flask_limiter - a ready to go package that can protect backend from spam requests. The default request limits per user are **2000 per day** or **500 per hour**. Limits for specific routes are given below:
#### Table of limits
| Route | Requests per minute |
| ----- | ----- |
| /signup | 60 |
| /signin | 60 |
| /update_exposure | 30 |
| /edit_submission | 60 |
| /search | 100 |
| /password_reset | 30 |
| /update_username | 30 |
| /delete_account | 30 |


## <span style="color: #e8b600">Unit tests</span>
Currently Swappr has no unit tests. In the future proper testing should be executed using <b style="color: #68ba6a">pytest</b> library.

Nevertheless, a python script named **tcreatemocksubmissions.py** is designed to create mockups (that is random fake users and submitted houses), and then import them into **swappr.db** for testing purposes.

To do that run:

```sh
python app.py -m MOCKUPSGEN MOCKUPSGEN
```
or
```sh
python app.py --mockupsgen MOCKUPSGEN MOCKUPSGEN
```
where the first MOCKUPSGEN is an integer that determines the number of mockup users, while the second one determines the number of mockup submitted houses. Submitted houses number can't exceed the number of users - if so the script handles the arguments to set them as equals.

By default the only static username that is created is **admin** and developers should use it for debugging.

#### Testing credentials
| Username | Password |
| -------- | -------- |
|  admin   |    admin     |


It is recommended to generated some thousands of mockups to have a chance in getting matching houses

## <span style="color: #e8b600">Python dependencies</span>
Below are enlisted all the Python frameworks, libraries and packages needed for this application.
- <b style="color: #68ba6a">json </b>
- <b style="color: #68ba6a">secrets </b>
- <b style="color: #68ba6a">subproccess </b>
- <b style="color: #68ba6a">loguru </b>
- <b style="color: #68ba6a">datetime </b>
- <b style="color: #68ba6a">argparse </b>
- <b style="color: #68ba6a">flask </b>
- <b style="color: #68ba6a">flask_limiter </b>
- <b style="color: #68ba6a">werkzeug.security </b>
- <b style="color: #68ba6a">string </b>
- <b style="color: #68ba6a">sqlite3 </b>
- <b style="color: #68ba6a">re </b>
- <b style="color: #68ba6a">functools </b>
- <b style="color: #68ba6a">tqdm </b>
- <b style="color: #68ba6a">random </b>
- <b style="color: #68ba6a">fictional_names </b>

Frameworks, libraries, and packages that are not embedded in Python3 should be installed using **requirements.txt** as previously in this article mentioned.


## <span style="color: #e8b600">Custom modules</span>
Swappr uses custom modules that hold constant variables and functions to be called in **app.py**. What follows is the description of these modules in separate section parts.
    
### <span style="color: #c9b7a4">argparser.py</span>
This module uses <span style="color: #68ba6a">argparse</span> Python package to create argument option instances. Added argument are stored in argparser variable, which is imported in whatever .py module is needed. You may check the argument options on section <b style="color: #eedebf">Running the app</b>, in <b style="color: #eedebf">Argument parser</b> block.

<hr>

### <span style="color: #c9b7a4">faccount.py</span>
Contains functions needed in **/account** route.
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`password_reset_validation`** | (oldpassword, new_password, confirm_new_password, hash) | Checks password reset input validityn | None | `check_password_hash`<sup>1</sup> `strong_password`<sup>2</sup> |
| **`update_username_validation`** | (new_username, user_id) | Checks password reset input validity | None | `username_exists`<sup>2</sup> |
| **`delete_account_validation`** | (delete_account_confirmation, email) | Checks email input validity for account deletion | None | None |

**Sources**: <sup>1</sup>werkzeug.security package, <sup>2</sup>fhelpers.py

<hr>

### <span style="color: #c9b7a4">fhelpers.py</span>
Contains functions needed in many routes.
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`cursor_execute`** | (query, *args) | Dynamically executes SQLite3 queries | `create_database_tables` | None |
| **`cursor_fetch`** | (query, *args) | Dynamically fetches data SQLite3 database | `create_database_tables` | `tuples_to_dict` |
| **`tuples_to_dict`** | (keys_tuple, values_tuple) | Converts two tuples into one dictionary | `cursor_fetch` | None |
| **`strong_password`** | (password) | Checks if a password is strong enough | `signup_validation`<sup>1</sup> `password_reset_validation`<sup>2</sup> | None |
| **`email_exists`** | (email) | Checks if email already exists in the database | `signup_validation`<sup>1</sup> | None |
| **`username_exists`** | (username, *args) | Checks if username already exists in the database | `signup_validation`<sup>1</sup> `update_username_validation`<sup>2</sup> | None |
| **`get_list_of_values`** | (json_data, column_name) | Converts a json file into a list with values of the selected column | `validate_submitted_location`<sup>3</sup> `validate_searched_location`<sup>4</sup> | None |
| **`check_submitted_location`** | (submitted_value, valid_values, error_message) | Checks submitted location validity | `validate_submitted_location`<sup>3</sup> `validate_searched_location`<sup>4</sup> | None |
| **`login_required`** | (f) | Decorate routes to require login | None | `decorated_function` |
| **`comma`** | (integer) | Formats an integer by placing commas between thousands | None | None |
| **`whitespace`** | (text) | Formats a snakecase string into a readable title | None | None |

**Sources**: <sup>1</sup>fsignup.py, <sup>2</sup>faccount.py, <sup>3</sup>fsubmit.py, <sup>4</sup>faccount.py

<hr>

### <span style="color: #c9b7a4">flog.py</span>
Contains constant variables and functions needed for history logger.
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`log`** | (message, level='INFO', indent=28) | Dynamically handles log indentations and message level | None | None |
| **`initialize_logger`** | None | Initializes loguru history logger | None | None |
| **`log_new_locations`** | (locations_update, new_locations_flag) | Add brief log info about newly inserted location entries in the database | None | None |

<hr>

### <span style="color: #c9b7a4">fsearch.py</span>
Contains the algorithmic functions and constant variables needed in **/search** route.
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`room_tolerance_factor`**   | (tolerance, room) | Returns the tolerance factor that adjusts the maximum value of the criteria search ranges | `tolerance_factors` | None |
| **`tolerance_factors`** | (tolerance) | Returns varied multipliers that affect the criteria ranges to be used in the matching score algorithm | None | `room_tolerance_factor` |
| **`criteria_ranges`** | (primary_submission, TOLERANCE_FACTORS) | Returns varied ranges to be used in the calculation of the matching score for each search house result | None | None |
| **`validate_searched_digits`** | (square_meters, rental, bedrooms, bathrooms) | Validates digit-required and ranged-required fields| `search_validation` | None |
| **`validate_searched_location`** | (city, municipality, region) | Validates location input | `search_validation` | `cursor_fetch`<sup>1</sup> `get_list_of_values`<sup>1</sup> `check_submitted_location`<sup>1</sup> |
| **`search_validation`** | (exposure, house_type, square_meters, rental, bedrooms, bathrooms, city, municipality, region) | Validates input data | None | `validate_searched_digits` `validate_searched_location` |
| **`calculate_location_matching_score`** | (result, primary_submission) | Calculates and returns a location matching score | `location_matching` | None |
| **`location_matching`** | (primary_submission, search_results) | Iterates all search results and adds into them the calculated location matching score | None | `calculate_location_matching_score` |
| **`calculate_house_matching_score`** | (result, CRITERIA_RANGES) | Calculates and returns a house characteristics matching score | None | **`house_matching`** |
| **`house_matching`** | (search_results, CRITERIA_RANGES) | Iterates all search results and adds into them the calculated house characteristics matching score | None | `calculate_house_matching_score` |
| **`matching_summary`** | (search_results) | Iterates all search results and adds into them the summary matching score | None | None |

**Source:** <sup>1</sup>fhelpers.py

<hr>

### <span style="color: #c9b7a4">fsignin.py</span>
Contains a function needed in **/signin** route.
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`signin_validation`** | (username, password, user_data) | Validates login credentials | None | <sup>1</sup>`check_password_hash` |

**Source**: <sup>1</sup>werkzeug.security package

<hr>

### <span style="color: #c9b7a4">fsignup.py</span>
Contains a function needed in **/signup** route.
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`signup_validation`** | (email, username, password, confirm_password) | Validates signup credentials | None | <sup>1</sup>`strong_password` <sup>1</sup>`email_exists` <sup>1</sup>`username_exists` |

**Source**: <sup>1</sup>fhelpers.py

<hr>

### <span style="color: #c9b7a4">fSQL.py</span>
Contains functions needed in database structuring.
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`create_database_tables`** | None | Creates database schema | None | <sup>1</sup>`cursor_execute` |
| **`import_locations`** | None | Syncs new entries between location.json and swappr.db | None | None |

<hr>

### <span style="color: #c9b7a4">fsubmit.py</span>
Contains constant variables and functions needed in both **/submit** and **edit_submission** routes.
#### Table of functions
| Function name | Parameters | Description | Child of | Parent of |
| ------------- | ---------- | ----------- | -------- | --------- |
| **`validate_submitted_digits`** | (square_meters, rental, bedrooms, bathrooms) | Creates database schema | None | <sup>1</sup>`cursor_execute` |
| **`import_locations`** | None | Validates digit-required and ranged-required fields | None | None |
| **`validate_submitted_location`** | (city, municipality, region) | Validates location input | `search_validation` | `get_list_of_values`<sup>1</sup> `check_submitted_location`<sup>1</sup> `cursor_fetch`<sup>1</sup> |
| **`submission_validation`** | (all_field_values, exposure, house_type, square_meters, rental, bedrooms, bathrooms, city, municipality, region, city_destination, municipality_destination, region_destination) | Validates input data | None | `validate_submitted_digits` `validate_submitted_location` |
| **`user_submissions_exist`** | (user_id) | Checks if user has at least one primary submission | `determine_primary_submission_status` | `cursor_fetch` |
| **`determine_primary_submission_status`** | (primary_submission, primary_submission_locked, user_id) | Determines primary submission status | None | `user_submissions_exist` `cursor_execute` |
| handle_primary_submission_upon_deletion | (submission_id, user_id) | Handles primary submission in database upon submission deletion | None | `cursor_fetch`<sup>1</sup> `cursor_execute`<sup>1</sup> |

**Source**: <sup>1</sup>fhelpers.py
