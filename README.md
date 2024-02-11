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
Swappr repo comes with no **.db** and **.log** files. These necessities will be created on program initialization. To initiate swappr run:
```sh
python app.py
```
But before running the program for the first time, Make sure that you have created a virtual environment and have installed all Python dependencies.

### Create a virtual invornment
To run swappr it is recommended to create a virtual environment where all Python dependencies will be installed.
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
Swappr comes with an embedded argument parser and developers can check their options using `python app.py -h`. Some of these options are:

- `-d` or `--debug` enables Flask's embedded debug mode for testing purposes
- `-b` or `--backup` runs automated backup routines for the database and log files
- `-l` or `--limiter` enables a request limiter to protect the backend from spam
- `-p` or `--premademockups` inserts a premade JSON of mockup users and submitted houses into the database. The premade mockups are tailored in such way so the developer could test the matching algorithm for every probable house **location/desired move location** between two Swappr users
- `-m [INTEGER INTEGER]` or `--mockup [INTEGER INTEGER]` creates mockup users and submitted houses to test matching algorithm. First integer is the number of users to be created, while the second is the number of the submitted houses. Submitted houses can't exceed the number of the mockup users - if so the program will limit submitted houses to be equal to users. As greater the numbers of the generated mockups, as greater the chance to catch a matching house while testing. *3000+ mockups are recommended*


## Developing tools
To create this app the following programming languages, frameworks, and dev tools were used:

- **Python3** and **Flask** mini framework package for the backend
- **HTML**/**CSS Bootstrap 5.2**/**JavaScript** for the frontend
- **Jinja2** for the HTML templates
- **AJAX** for asynchronous request logic
- **SQLite3** for the database handling
- **Bash** for backup functionalities
- **noUiSlider JavaScript** package to control input values for searching filters
- **jQuery.validate** package for extra frontend validation


Backend convention relies on splitted .py files where the proper code for every related section is contained. Python files are described as follows:

- app.py: This is the main file where the initialization of the program takes place and routes are created for every web app section. Most routes have their corresponding .py file where their dependent functions are present. For instance <b>/search</b> route calls some functions that are imported from <b>fsubmit.py</b>, while <b>/signup</b> route draws functions from <b>fsignup.py</b>, and so on...
- argparser.py:

## Validation
Swappr uses validation logic for whatever input data the user's may send with their request. This validation takes place in frontend using html browser validation, jQuery.validate() methods, and custom JavaScript functions, while custom python functions are protecting the backend.