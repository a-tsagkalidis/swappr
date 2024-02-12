# Swappr
**Author**: Argyrios Tsagkalidis

**Location**: Thessaloniki, Greece

**License**: MIT

**Video Demo**:  <URL HERE>

## Description
Swappr is a web app project that helps the users to swap their rented houses.

The users create an account, uploads their rented house's specifications, and explore potential matches for a hassle-free swap experience.

The app uses an intelligent algorithm that suggests compatible house swap options, ensuring that the user's preferences align with potential matches. The algorithm uses a matching score based on house characteristics, house location, and desired move destination.

## Running the app
Swappr repo comes with no **.db** or **.log** files. These necessities will be created on program initialization. To initiate swappr run:
```sh
python app.py
```
But before you run the program for the first time, make sure that you have created a virtual environment and have installed all Python dependencies.

### Create a virtual environment
Before you run Swappr it is recommended to create a virtual environment where all Python dependencies will be installed.
While in working directory run:
```sh
python -m venv .venv
```
Notice that a `.venv` folder has been created.

### Install Python dependencies
After your venv creation, you should install all swappr Python dependencies. While in working directory run:
```sh
pip install -r requirements.txt
``` 

### Argument parser
Swappr comes with an embedded argument parser and developers can check its options using `python app.py -h`. Optinal arguments are:

- `-d` or `--debug` enables Flask's embedded debug mode for testing purposes
- `-b` or `--backup` runs automated backup routines for the database and log files
- `-l` or `--limiter` enables a request limiter to protect the backend from spam
- `-p` or `--premademockups` inserts a premade JSON of mockup users and submitted houses into the database. The premade mockups are tailored in such way so that developers can test the matching algorithm for every probable **location/desired move location** scenario
- `-m INTEGER INTEGER` or `--mockupsgen INTEGER INTEGER` creates mockup users and submitted houses to test the matching algorithm. First integer is the number of users to be created, while the second is the number of the submitted houses. Submitted houses can't exceed the number of the mockup users - if so the program will limit submitted houses equal to users. The higher the number of mockups created, the higher the chance of catching a matching house during the test. *Recommended 3000+ Mockups*


## Developing tools
Swappr uses the following programming languages, frameworks, and dev tools:

- **Python3** and **Flask** mini framework package for the backend
- **HTML**/**CSS Bootstrap 5.2**/**JavaScript** for the frontend
- **Jinja2** for the HTML templates
- **AJAX** for asynchronous request logic
- **SQLite3** for the database handling
- **Bash** for backup functionalities
- **noUiSlider JavaScript** package to control input values for searching filters
- **jQuery.validate** package for extra frontend validation

## Backend
Backend convention relies on splitted .py files where the proper code for every related section is contained. Python files are described as follows:

### app.py
This is the main file where Swappr initialization takes place and the routes for all sections are created.

#### Swappr initialization
When **app.py** initiates the following functionalities take action:
- Configures a logger using loguru library
- Checks for given arguments such as `--backup`, `--limiter`, and/or `--premademockups`/`--mockupsgen INTEGER INTEGER` to call the corresponding functions.
- Checks if SQL database is present or else it creates it with the proper schema in **swappr.db**
- Checks if `locations` table in **swappr.db** matches with all the data in `locations.json` file. If new locations are present in the JSON file, then they are imported as new entries in **swappr.db** `locations` table

#### Route creation
Most routes have their corresponding .py file where their dependent functions are present. For instance **/search** route calls some functions that are imported from **fsearch.py**, while **/signup** route draws functions from **fsignup.py**, and so on...

    
- argparser.py:

## Validation
Swappr uses validation logic for whatever input data the user's may send with their request. This validation takes place in frontend using html browser validation, jQuery.validate() methods, and custom JavaScript functions, while custom python functions are protecting the backend.