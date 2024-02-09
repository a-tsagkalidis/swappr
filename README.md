# swappr
#### Video Demo:  <URL HERE>
#### Description:


Swappr is a web app project that helps the users to swap their houses.

The users create an account, uploads their rented house's specifications, and explore potential matches for a hassle-free swap experience.

The app uses an intelligent algorithm that suggests compatible house swap options, unsuring that the user's preferences align with potential matches. The algorithm uses a matching score based on house characteristics, house location, and desired move destination.

Swappr uses validation logic for whatever input data the user's may send with their request. This validation takes place in frontend using html browser validation, jQuery.validate() methods, and custom JavaScript functions, while custom python functions are protecting the backend.

Swappr comes with an embedded argument parser and developers can check their options using `python app.py -h`. Some of these options are:
<ul>
    <li>Enable a request limiter to protect the backend from spam</li>
    <li>Run automated database and log backup routines<li>
    <li>Create mockup users and submitted houses to test matching algorithm</li>
</ul>

To create this app the following languages and tools were used:
<ul>
    <li>Python3 and Flask mini framework package for the backend</li>
    <li>HTML/CSS with Bootstrap 5.2/JavaScript and jQuery.validate package for the frontend<li>
    <li>SQLite3 for the database</li>
    <li>Bash for backup functionalities</li>
    <li>noUiSlider JavaScript package to control input values for searching filters</li>
</ul>

Backend logic has been splitted in many .py files where the proper code for every related section is contained. Python files are described as follows:
<ul>
    <li>app.py: Routing logic division for every web app section. The convention is that almost every route has its corresponding .py file where related functions are present. For instance <b>/search</b> route calls some functions that are imported from <b>fsubmit.py</b>, while <b>/signup</b> route draws functions from <b>fsignup.py</b>, and so on...
    <li>