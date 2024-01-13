// ----- BACK-TO-TOP BUTTON ----- //
// Asign a variable with the top-button id
let topButton = document.getElementById("top-button");

/**
 * A function that scrolls the webpage at the top
 */
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}


// ----- SIGN UP VALIDATION FORM ----- //
function validateSignUpForm() {
    const signupForm = document.querySelector('#signupForm');
    var email = signupForm.elements["email"].value;
    var username = signupForm.elements["username"].value;
    var password = signupForm.elements["password"].value;
    var confirmPassword = signupForm.elements["confirmPassword"].value;

    // Ensure form input types are as they should be
    formElementsTypes = [
        signupForm.elements["email"].type,
        signupForm.elements["username"].type,
        signupForm.elements["password"].type,
        signupForm.elements["confirmPassword"].type,
    ];

    expectedTypes = [
        "email",
        "text",
        "password",
        "password",
    ];

    for (let i = 0; i < formElementsTypes.length; i++) {
        if (formElementsTypes[i] !== expectedTypes[i]) {
            alert("Unkown error occured!!");
            return false;
        }
    }

    // Ensure fields are not blank
    if (email === "" || username === "" || password === "" || confirmPassword === "") {
        alert("Please fill in all the required fields.");
        return false;
    }

    // Ensure email adress has valid chars
    var emailRegexStipulations = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegexStipulations.test(email)) {
        alert('Please enter a valid email address.');
        return false;
    }

    // Ensure username is at least 3 characters long
    if (username.length < 3) {
        alert('Username must be at least 3 characters long.');
        return false;
    }

    // Ensure username does not contain any punctuation characters or whitespaces
    var invalidCharactersRegex = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\s]/;
    if (invalidCharactersRegex.test(username)) {
        alert('Username cannot contain punctuation characters or whitespaces.');
        return false;
    }

    // Ensure password and confirmation match
    if (password !== confirmPassword) {
        alert("Password and password confirmation do not match.");
        return false;
    }

    // // Ensure password is strong
    // var passwordRegexStipulations = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[\w!@#$%^&*()_+]{8,}$/;
    // if (!passwordRegexStipulations.test(password)) {
    //     alert("Password must be at least 8 characters long, including at least 1 uppercase letter, 1 lowercase letter, a decimal number, and a punctuation character.");
    //     return false;
    // }

    // Validation successfully passed
    return true;
}


// ----- SIGN IN VALIDATION FORM ----- //
function validateSignInForm() {
    const signinForm = document.querySelector('#signinForm');
    var username = signinForm.elements["username"].value;
    var password = signinForm.elements["password"].value;

    // Ensure fields are not blank
    if (username === "" && password === "") {
        alert("Please fill in your username and password.");
        return false;
    }

    // Ensure fields are not blank
    if (username === "") {
        alert("Please fill in your username.");
        return false;
    }

    // Ensure fields are not blank
    if (password === "") {
        alert("Please fill in your password.");
        return false;
    }

    // Ensure username does not contain any punctuation characters
    var punctuationRegexStipulations = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]/;
    if (punctuationRegexStipulations.test(username)) {
        alert('Username cannot contain punctuation characters.');
        return false;
    }

    // Validation successufully passed
    return true;
}


// ----- SUBMIT AND EDIT_SUBMISSION FIELD HANDLING AND VALIDATION ----- //
// Function to enforce min and max values
function enforceMinMax(input, min, max) {
    var value = parseInt(input.value, 10);
    if (isNaN(value) || value < min) {
        input.value = min;
    } else if (value > max) {
        input.value = max;
    }
}

// Event listener for handling backspace key special case
function handleBackspace(input, minValue) {
    input.addEventListener('keydown', function (event) {
        if (event.key === 'Backspace' && parseInt(input.value, 10) === minValue) {
            input.value = '';  // Clear the input
        }
    });
}

function validateSubmitForm() {
    const submitForm = document.querySelector('.submitForm');
    const exposure = submitForm.elements["exposure"].value;
    const houseType = submitForm.elements["houseType"].value;
    const squareMeters = submitForm.elements["squareMeters"].value;
    const rental = submitForm.elements["rental"].value;
    const bedrooms = submitForm.elements["bedrooms"].value;
    const bathrooms = submitForm.elements["bathrooms"].value;
    const inputFormValues = [
        exposure,
        houseType,
        squareMeters,
        rental,
        bedrooms,
        bathrooms,
    ];

    // Ensure input fields are not blank
    for (let i = 0; i < inputFormValues.length; i++) {
        if (inputFormValues[i] === '') {
            alert('Please fill in all the required fields.');
            return false;
        }
    }

    // Ensure exposure is either 'public' or 'private'
    if (exposure !== 'public' && exposure !== 'private') {
        alert('Invalid exposure value.');
        return false;
    }

    // Ensure houseType is a valid option
    const validHouseTypes = [
        'studio',
        'flat',
        'maisonette',
        'semi-detached_house',
        'detached_house',
        'mansion',
    ]
    if (!validHouseTypes.includes(houseType)) {
        alert('Invalid house type.');
        return false;
    }

    // Ensure countable inputs type are numbers
    const mustBeNumbers = [
        submitForm.elements["squareMeters"],
        submitForm.elements["rental"],
        submitForm.elements["bedrooms"],
        submitForm.elements["bathrooms"],
    ]
    for (let i = 0; i < mustBeNumbers.length; i++) {
        if (mustBeNumbers[i].type !== 'number') {
            alert("Invalid number.");
            return false;
        }
    }

    // Ensure countable inputs are within limits
    if (squareMeters < 0 || squareMeters > 1000) {
        alert('Invalid square meters');
        return false;
    }

    if (rental < 0 || rental > 10000) {
        alert('Invalid rental value');
        return false;
    }

    if (bedrooms < 0 || bedrooms > 10) {
        alert('Invalid bedroom quantity');
        return false;
    }

    if (bathrooms < 0 || bathrooms > 10) {
        alert('Invalid bathroom quantity');
        return false;
    }

    // Validation successufully passed
    return true;
};


// Execute the following code only for submit, edit_submission, and search routes
if (window.location.pathname === '/submit' ||
    window.location.pathname === '/edit_submission' ||
    window.location.pathname === '/search'
) {
    // Event listener for "squareMeters" input
    document.getElementById('squareMeters').addEventListener('input', function () {
        enforceMinMax(this, 0, 1000);
    });

    // Event listener for "rental" input
    document.getElementById('rental').addEventListener('input', function () {
        enforceMinMax(this, 0, 10000);
    });

    // Event listener for "bedrooms" input
    document.getElementById('bedrooms').addEventListener('input', function () {
        enforceMinMax(this, 0, 10);
    });

    // Event listener for "bathrooms" input
    document.getElementById('bathrooms').addEventListener('input', function () {
        enforceMinMax(this, 0, 10);
    });

    // Call the function for each input
    handleBackspace(document.getElementById('bedrooms'), 0);
    handleBackspace(document.getElementById('bathrooms'), 0);
    handleBackspace(document.getElementById('squareMeters'), 0);
    handleBackspace(document.getElementById('rental'), 0);

    // ----- DYNAMIC SELECT OPTIONS -----//
    // Fetch municipalities based on the selected city
    document.getElementById('city').addEventListener('change', function () {
        const selectedCity = this.value;

        // Reset municipality and region selectors
        document.getElementById('municipality').innerHTML = '<option value="">Select Municipality</option>';
        document.getElementById('region').innerHTML = '<option value="">Select Region</option>';

        // If the selected city is the default value, no need to fetch data
        if (selectedCity === "") {
            return;
        }

        // Fetch municipalities based on the selected city
        fetch(`/get_municipalities?city=${selectedCity}`)
            .then(response => response.json())
            .then(data => {
                const municipalitySelect = document.getElementById('municipality');
                municipalitySelect.innerHTML = '<option value="">Select Municipality</option>';
                data.forEach(municipalityObject => {
                    const option = document.createElement('option');
                    option.value = municipalityObject.municipality;
                    option.textContent = whitespace(municipalityObject.municipality);
                    municipalitySelect.appendChild(option);
                });
            });
    });

    // Fetch regions based on the selected municipality
    document.getElementById('municipality').addEventListener('change', function () {
        const selectedMunicipality = this.value;
        const selectedCity = document.getElementById('city').value;

        // Reset region selector
        document.getElementById('region').innerHTML = '<option value="">Select Region</option>';

        // If the selected municipality is the default value, no need to fetch data
        if (selectedMunicipality === "") {
            return;
        }

        // Fetch regions based on the selected city and municipality
        fetch(`/get_regions?city=${selectedCity}&municipality=${selectedMunicipality}`)
            .then(response => response.json())
            .then(data => {
                const regionSelect = document.getElementById('region');
                regionSelect.innerHTML = '<option value="">Select Region</option>';
                data.forEach(regionObject => {
                    const option = document.createElement('option');
                    option.value = regionObject.region;
                    option.textContent = whitespace(regionObject.region);
                    regionSelect.appendChild(option);
                });
            });
    });
}


function whitespace(text) {
    return text.replace(/_/g, ' ').replace(/\w\S*/g, function (word) {
        return word.charAt(0).toUpperCase() + word.substr(1).toLowerCase();
    });
}


if (window.location.pathname === '/search') {
    var arbitraryValuesSlider = document.getElementById('squareMetersSlider');
    var arbitraryValuesForSlider = ['100', '200', '300', '400', '500', '600'];

    var format = {
        to: function(value) {
            return arbitraryValuesForSlider[Math.round(value)];
        },
        from: function (value) {
            return arbitraryValuesForSlider.indexOf(value);
        }
    };

    noUiSlider.create(arbitraryValuesSlider, {
        // start values are parsed by 'format'
        start: ['100', '500'],
        range: { min: 0, max: arbitraryValuesForSlider.length - 1 },
        step: 1,
        tooltips: true,
        format: format,
        // pips: { mode: 'steps', format: format, density: 50 },
    });

    var snapValues = [
        document.getElementById('squareMetersMinimum'),
        document.getElementById('squareMetersMaximum')
    ];

    // Update sliders
    arbitraryValuesSlider.noUiSlider.on('update', function (values, handle) {
        snapValues[handle].innerHTML = values[handle];

        // Update the hidden input field
        document.getElementById('squareMeters').value = JSON.stringify({ min: values[0], max: values[1] })
    });
}
