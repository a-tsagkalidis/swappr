// Constant variables for inputs that require numbers
const squareMetersMin = 30;
const squareMetersMax = 200;
const rentalMin = 100;
const rentalMax = 2000;
const bedroomsMin = 1;
const bedroomsMax = 4;
const bathroomsMin = 1;
const bathroomsMax = 2;


/** ||||| [0.0] @all ROUTES COMMON HELPERS ||||| */
// ----- [0.1] BACK-TO-TOP BUTTON ----- //
/** [0.1.1]
 * A function that scrolls the webpage at the top. It is called whenever the
 * button `Back to top` us pressed (onclick). This button is present in every
 * route, because it is implemented in `layout.html`.
 */
function topFunction() {
	document.body.scrollTop = 0;
	document.documentElement.scrollTop = 0;
}

// Asign a variable with the top-button id from `layout.html`
let topButton = document.getElementById("top-button");

/** [0.1.2]
 * A function that dismisses any Flask flash message from the UI after 3 seconds.
 * This function is called in every route. I is useful because the flash messages
 * are implemented in `layout.html` and can occur in every other route.
 */
function dismissFlashMessage(timeout) {
	// Select the flash message element
	const flashMessage = document.getElementById('flashMessage');

	// Check if the flash message element exists
	if (flashMessage) {
		// Set a timeout to remove the flash message after 3 seconds
		setTimeout(() => {
			flashMessage.remove();
		}, timeout);
	}
}

// Call the function that dismisses Flask flash messages after given time 
dismissFlashMessage(4000)



/** ||||| [1.0] @signup ROUTE ||||| */
// ----- [1.1] SIGNUP FORM VALIDATION ----- //
/** [1.1.1]
 * A function that fetches all the user input from the filled input fields and
 * ensures they are of proper and valid values.
 * It is called when `Sign Up` button is clicked (onsubmit) in signup.html forms.
 */
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
	var passwordRegexStipulations = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[\w!@#$%^&*()_+]{8,}$/;
	if (!passwordRegexStipulations.test(password)) {
		alert("Password must be at least 8 characters long, including at least 1 uppercase letter, 1 lowercase letter, a decimal number, and a punctuation character.");
		return false;
	}

	// Validation successfully passed
	return true;
}


/** [1.1.2]
 * A jQuery function that validates realtime the signup route form
 */
function jQueryValidateSignUpForm() {
	$(function () {
		jQuery.validator.addMethod("password", function (value, element) {
			var passwordRegexStipulations = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[\w!@#$%^&*()_+]{8,}$/;
			var result = this.optional(element) ||
				value.length >= 8 &&
				passwordRegexStipulations.test(value);
			return result;
		},
			`Password must be at least 8 characters long containing at least
			an uppercase, a lowercase, a symbol, and a number.`
		);

		jQuery.validator.addMethod("text", function (value, element) {
			var invalidCharactersRegex = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\s]/;
			var result = this.optional(element) ||
				value.length >= 3 &&
				!invalidCharactersRegex.test(value);
			return result;
		},
			`Username must be at least 3 characters long and cannot contain
			punctuation characters or whitespaces.`
		);

		$("#signupForm").validate({
			rules:
			{
				email:
				{
					required: true,
					email: true
				},
				username:
				{
					required: true
				},
				password:
				{
					required: true
				},
				confirmPassword:
				{
					required: true,
					equalTo: "#password"
				}
			},
			messages:
			{
				email: {
					required: "This field is required",
					email: "Please enter a valid email address, example: you@yourdomain.com"
				},
				username:
				{
					required: "This field is required",
				},
				password:
				{
					required: "This field is required",
				},
				confirmPassword: {
					required: "This field is required",
					equalTo: "Please enter the same password as above"
				}
			}
		});
	});
}


// ----- [1.2] EXECUTES WHEN SIGNUP ROUTE LOADS -----//
// Execute the following code only for signup route
$(document).ready(function () {
	if (
		window.location.pathname === '/signup'
	) {
		jQueryValidateSignUpForm()
	}

	// Re-execute validation if form is submitted or changed
	$("#signupForm").on("submit", function () {
		jQueryValidateSignUpForm();
	});
	$("#signupForm").on("change", function () {
		jQueryValidateSignUpForm();
	});
});



/** ||||| [2.0] @signin ROUTE ||||| */
// ----- [2.1] SIGNIN FORM VALIDATION ----- //
/** [2.1.1]
 * A function that fetches all the user input from the filled input fields and
 * ensures they are of proper and valid values.
 * It is called when `Sign In` button is clicked (onsubmit) in signin.html form.
 */
function validateSignInForm() {
	const signinForm = document.querySelector('#signinForm');
	var username = signinForm.elements["username"].value;
	var password = signinForm.elements["password"].value;

	// Ensure email and username fields are not blank
	if (username === "" && password === "") {
		alert("Please fill in your username and password.");
		return false;
	}

	// Ensure email field is not blank
	if (username === "") {
		alert("Please fill in your username.");
		return false;
	}

	// Ensure username field is not blank
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


/** [2.1.2]
 * A jQuery function that validates realtime the signin route form
 */
function jQueryValidateSignInForm() {
	$(function () {
		jQuery.validator.addMethod("text", function (value, element) {
			var invalidCharactersRegex = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\s]/;
			var result = this.optional(element) ||
				value.length >= 3 &&
				!invalidCharactersRegex.test(value);
			return result;
		},
			`Your username is at least 3 characters long and does not contain
			punctuation characters or whitespaces.`
		);

		$("#signinForm").validate({
			rules:
			{
				username:
				{
					required: true
				},
				password:
				{
					required: true
				}
			},
			messages:
			{
				username:
				{
					required: "This field is required",
				},
				password:
				{
					required: "This field is required",
				}
			}
		});
	});
}


// ----- [2.2] EXECUTES WHEN SIGNIN ROUTE LOADS -----//
// Execute the following code only for signin route
$(document).ready(function () {
	if (
		window.location.pathname === '/signin'
	) {
		jQueryValidateSignInForm()
	}

	// Re-execute validation if form is submitted or changed
	$("#signinForm").on("submit", function () {
		jQueryValidateSignInForm();
	});
	$("#signinForm").on("change", function () {
		jQueryValidateSignInForm();
	});
});




/** ||||| [3.0] @submit and @edit_submission ROUTES ||||| */
// ----- [3.1] SUBMIT/EDIT_SUBMISSION FORM VALIDATION ----- //
/** [3.1.1]
 * A function that fetches all the user input from the filled input fields and
 * ensures they are of proper and valid values.
 * It is called when `Submit` or `Save` buttons are clicked (onsubmit) in
 * submit.html and edit_submission.html forms.
 */
function validateSubmitForm() {
	const submitForm = document.querySelector('#submitForm');
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
	if (squareMeters < squareMetersMin || squareMeters > squareMetersMax) {
		alert('Invalid square meters');
		return false;
	}

	if (rental < rentalMin || rental > rentalMax) {
		alert('Invalid rental value');
		return false;
	}

	if (bedrooms < bedroomsMin || bedrooms > bedroomsMax) {
		alert('Invalid bedroom quantity');
		return false;
	}

	if (bathrooms < bathroomsMin || bathrooms > bathroomsMax) {
		alert('Invalid bathroom quantity');
		return false;
	}

	// Validation successufully passed
	return true;
};


// ----- [3.2] QUANTITY LIMITER VALIDATOR ----- //
/** [3.2.1]
 * jQuery function validates @submit and @edit_submisson forms.
 * It is called when id #submitForm is present in the html
 */
function jQueryValidateSubmitForm() {
	$(function () {
		$("#submitForm").validate({
			rules:
			{
				squareMeters:
				{
					range: [squareMetersMin, squareMetersMax],
					required: true,
					number: true
				},
				rental:
				{
					range: [rentalMin, rentalMax],
					required: true,
					number: true
				},
				bedrooms:
				{
					range: [bedroomsMin, bedroomsMax],
					required: true,
					number: true
				},
				bathrooms:
				{
					range: [bathroomsMin, bathroomsMax],
					required: true,
					number: true
				},
				city:
				{
					required: true,
				},
				municipality:
				{
					required: true,
				},
				region:
				{
					required: true,
				},
				cityDestination:
				{
					required: true,
				},
				municipalityDestination:
				{
					required: true,
				},
				regionDestination:
				{
					required: true,
				},
				exposure:
				{
					required: true
				},
				primarySubmissionLocked:
				{
					required: true
				}
			},
			messages:
			{
				squareMeters:
				{
					required: "This field is required",
					min: `Should be greater than or equal to ${squareMetersMin}`,
					max: `Should be less than or equal to ${squareMetersMax}`,
					number: `Choose between ${squareMetersMin} and ${squareMetersMax}`
				},
				rental:
				{
					required: "This field is required",
					min: `Should be greater than or equal to ${rentalMin}`,
					max: `Should be less than or equal to ${rentalMax}`,
					number: `Choose between ${rentalMin} and ${rentalMax}`
				},
				bedrooms:
				{
					required: "This field is required",
					min: `Should be greater than or equal to ${bedroomsMin}`,
					max: `Should be less than or equal to ${bedroomsMax}`,
					number: `Choose between ${bedroomsMin} and ${bedroomsMax}`
				},
				bathrooms:
				{
					required: "This field is required",
					min: `Should be greater than or equal to ${bathroomsMin}`,
					max: `Should be less than or equal to ${bathroomsMax}`,
					number: `Choose between ${bathroomsMin} and ${bathroomsMax}`
				},
				city:
				{
					required: "This field is required"
				},
				municipality:
				{
					required: "This field is required"
				},
				region:
				{
					required: "This field is required"
				},
				cityDestination:
				{
					required: "This field is required"
				},
				municipalityDestination:
				{
					required: "This field is required"
				},
				regionDestination:
				{
					required: "This field is required"
				},
				exposure:
				{
					required: "This field is required"
				},
				primarySubmissionLocked:
				{
					required: "This field is required"
				}
			}
		});
	});
}



// ----- [3.3] DYNAMIC SELECT OPTIONS -----//
/** [3.3.1]
 * A function that replaces underscores with whitespaces and lowercased words 
 * to titles. It is called in function [3.3.2].
 */
function whitespace(text) {
	return text.replace(/_/g, ' ').replace(/\w\S*/g, function (word) {
		return word.charAt(0).toUpperCase() + word.substr(1).toLowerCase();
	});
}


/** [3.3.2]
 * This functions sets a triplet of selectors to work dynamically based on the
 * user's previous selections. It is called in [3.4].
 */
function initializeLocationSelectors(cityId, municipalityId, regionId) {
	// Check if city selector has changed and populate municipalities selector
	document.getElementById(cityId).addEventListener('change', function () {
		const selectedCity = this.value;

		// Reset municipality and region selectors
		if (cityId === "cityDestination") {
			document.getElementById(municipalityId).innerHTML = '<option value="any">Any</option>';
			document.getElementById(regionId).innerHTML = '<option value="any">Any</option>';
		} else {
			document.getElementById(municipalityId).innerHTML = '<option value="">Select Municipality</option>';
			document.getElementById(regionId).innerHTML = '<option value="">Select Region</option>';
		}

		// If the selected city is the default value, no need to fetch data
		if (selectedCity === "" || selectedCity === "any") {
			return;
		}

		// Fetch municipalities based on the selected city
		fetch(`/get_municipalities?city=${selectedCity}`)
			.then(response => response.json())
			.then(data => {
				const municipalitySelect = document.getElementById(municipalityId);
				if (municipalityId === "municipalityDestination") {
					municipalitySelect.innerHTML = '<option value="any">Any</option>';
				} else {
					municipalitySelect.innerHTML = '<option value="">Select Municipality</option>';
				}
				data.forEach(municipalityObject => {
					const option = document.createElement('option');
					option.value = municipalityObject.municipality;
					option.textContent = whitespace(municipalityObject.municipality);
					municipalitySelect.appendChild(option);
				});
			});
	});

	// Check if municipality selector has changed and populate regions selector
	document.getElementById(municipalityId).addEventListener('change', function () {
		const selectedMunicipality = this.value;
		const selectedCity = document.getElementById(cityId).value;

		// Reset region selector
		if (municipalityId === "municipalityDestination") {
			document.getElementById(regionId).innerHTML = '<option value="any">Any</option>';
		} else {
			document.getElementById(regionId).innerHTML = '<option value="">Select Region</option>';
		}

		// If the selected municipality is the default value, no need to fetch data
		if (selectedMunicipality === "" || selectedMunicipality === "any") {
			return;
		}

		// Fetch regions based on the selected city and municipality
		fetch(`/get_regions?city=${selectedCity}&municipality=${selectedMunicipality}`)
			.then(response => response.json())
			.then(data => {
				const regionSelect = document.getElementById(regionId);
				if (regionId === "regionDestination") {
					regionSelect.innerHTML = '<option value="any">Any</option>';
				} else {
					regionSelect.innerHTML = '<option value="">Select Region</option>';
				}
				data.forEach(regionObject => {
					const option = document.createElement('option');
					option.value = regionObject.region;
					option.textContent = whitespace(regionObject.region);
					regionSelect.appendChild(option);
				});
			});
	});
}


// ----- [3.4] EXECUTES WHEN SUBMIT OR EDIT_SUBMISSION ROUTES LOAD -----//
// Execute the following code only for submit and edit_submission routes
$(document).ready(function () {
	if (
		window.location.pathname === '/submit' ||
		window.location.pathname === '/edit_submission'
	) {
		// Initialize location selectors
		initializeLocationSelectors(
			'city',
			'municipality',
			'region'
		);

		// Initialize location destination selectors
		initializeLocationSelectors(
			'cityDestination',
			'municipalityDestination',
			'regionDestination'
		);

		jQueryValidateSubmitForm()
	}

	// Re-execute validation if form is submitted or changed
	$("#submitForm").on("submit", function () {
		jQueryValidateSubmitForm();
	});
	$("#submitForm").on("change", function () {
		jQueryValidateSubmitForm();
	});
});




/** ||||| [4.0] @search ROUTE ||||| */
// ----- [4.1] NOUISLIDER CREATIONS ----- //
/** [4.1.1]
 * Function that is being called in noUiSliders creations [4.1.2]. Formats
 * values from 2 decimals (default) to 0 decimals.
 */
function createSliderFormat() {
	return {
		to: function (value) {
			return Math.round(value);
		},
		from: function (value) {
			return parseFloat(value);
		}
	};
}


/** [4.1.2]
 * Function to create noUiSliders. It is called in [4.2] to be loaded
 * in @search route
 */
function loadNoUiSliders() {
	// --- [4.1.2.a] Square Meters noUiSlider ---//
	// Get square meters slider from DOM
	var squareMetersSlider = document.getElementById('squareMetersSlider');

	// Create dual slider for square meters
	noUiSlider.create(squareMetersSlider, {
		start: [squareMetersMin, squareMetersMax],
		range: { min: squareMetersMin, max: squareMetersMax },
		step: 5,
		tooltips: false,
		format: createSliderFormat()
	});

	// Get an array of the minimum and maximum values of square meters from DOM 
	var squareMetersSnapValues = [
		document.getElementById('squareMetersMinimum'),
		document.getElementById('squareMetersMaximum')
	];

	// Update slider values
	squareMetersSlider.noUiSlider.on('update', function (values, handle) {
		squareMetersSnapValues[handle].innerHTML = values[handle];

		// Update the hidden input field that will send the values to backend
		document.getElementById('squareMeters').value = JSON.stringify({ min: values[0], max: values[1] })
	});


	// --- [4.1.2.b] Rental noUiSlider ---//
	// Get rental slider from DOM
	var rentalSlider = document.getElementById('rentalSlider');

	// Create dual slider for rental
	noUiSlider.create(rentalSlider, {
		start: [rentalMin, rentalMax],
		range: { min: rentalMin, max: rentalMax },
		step: 50,
		tooltips: false,
		format: createSliderFormat()
	});

	// Get an array of the minimum and maximum values of rental from DOM 
	var rentalSnapValues = [
		document.getElementById('rentalMinimum'),
		document.getElementById('rentalMaximum')
	];

	// Update slider values
	rentalSlider.noUiSlider.on('update', function (values, handle) {
		rentalSnapValues[handle].innerHTML = values[handle];

		// Update the hidden input field that will send the values to backend
		document.getElementById('rental').value = JSON.stringify({ min: values[0], max: values[1] })
	});


	// --- [4.1.2.c] Bedrooms noUiSlider ---//
	// Get bedrooms slider from DOM
	var bedroomsSlider = document.getElementById('bedroomsSlider');

	// Create dual slider for bedrooms
	noUiSlider.create(bedroomsSlider, {
		start: [bedroomsMin, bedroomsMax],
		range: { min: bedroomsMin, max: bedroomsMax },
		step: 1,
		tooltips: false,
		format: createSliderFormat()
	});

	// Get an array of the minimum and maximum values of bedrooms from DOM 
	var bedroomsSnapValues = [
		document.getElementById('bedroomsMinimum'),
		document.getElementById('bedroomsMaximum')
	];

	// Update slider values
	bedroomsSlider.noUiSlider.on('update', function (values, handle) {
		bedroomsSnapValues[handle].innerHTML = values[handle];

		// Update the hidden input field that will send the values to backend
		document.getElementById('bedrooms').value = JSON.stringify({ min: values[0], max: values[1] })
	});


	// --- [4.1.2.d] Bathrooms noUiSlider ---//
	// Get bathrooms slider from DOM
	var bathroomsSlider = document.getElementById('bathroomsSlider');

	// Create dual slider for bathrooms
	noUiSlider.create(bathroomsSlider, {
		start: [bathroomsMin, bathroomsMax],
		range: { min: bathroomsMin, max: bathroomsMax },
		step: 1,
		tooltips: false,
		format: createSliderFormat()
	});

	// Get an array of the minimum and maximum values of bathrooms from DOM 
	var bathroomsSnapValues = [
		document.getElementById('bathroomsMinimum'),
		document.getElementById('bathroomsMaximum')
	];

	// Update slider values
	bathroomsSlider.noUiSlider.on('update', function (values, handle) {
		bathroomsSnapValues[handle].innerHTML = values[handle];

		// Update the hidden input field that will send the values to backend
		document.getElementById('bathrooms').value = JSON.stringify({ min: values[0], max: values[1] })
	});


	// --- [4.1.2.e] Tolerance noUiSlider ---//
	// Get tolerance slider from DOM
	var toleranceSlider = document.getElementById('toleranceSlider');

	noUiSlider.create(toleranceSlider, {
		start: 10,
		behaviour: 'tap',
		step: 10,
		range: {
			'min': 10,
			'max': 100
		},
		format: createSliderFormat()
	});

	// Get an array of the minimum and maximum values of tolerance from DOM 
	var toleranceSnapValue = document.getElementById('toleranceOut');

	// Update slider values
	toleranceSlider.noUiSlider.on('update', function (value) {
		toleranceSnapValue.innerHTML = value;

		// Update the hidden input field that will send the values to backend
		document.getElementById('tolerance').value = value;
	});
}

/** [4.1.3]
 * Function that makes asyncronous POST requests in @search route to get
 * search results and load them in the html search results section
 */
function asynchronousSearch() {
	// Add an event listener to the search form
	document.getElementById('searchForm').addEventListener('submit', function (event) {
		// Prevent the default form submission to be loaded
		event.preventDefault();

		// Get the form data
		const formData = new FormData(this);

		// Make an AJAX POST request to the backend to get search results
		fetch('/search', {
			method: 'POST',
			body: formData
		})
			.then(response => response.text())
			.then(data => {
				// Load search results section with the response from backend
				document.getElementById('searchResults').innerHTML = data;
			})
			.catch(error => {
				console.error('Error:', error);
			});
	});
}


// ----- [4.2] EXECUTES WHEN SEARCH ROUTE LOADS -----//
// Execute the following code only for search route
$(document).ready(function () {
	if (window.location.pathname === '/search') {
		// Load noUiSliders
		loadNoUiSliders()

		// Initialize location selectors
		initializeLocationSelectors(
			'city',
			'municipality',
			'region'
		);

		// Call function for AJAX search result to operate
		asynchronousSearch()
	}
});



/** ||||| [5.0] @account ROUTE ||||| */
// ----- [5.1] UPDATE USERNAME -----//
/** [5.1.1]
 * A function that makes visible username edit. It is called when the user's
 * username is clicked (onclick) and shows the text field for the new username
 * (placeholder='Enter new username'), `Save` and `Cancel` buttons.
 */
function enableUsernameEdit() {
	document.getElementById('usernameContainer').style.display = 'none';
	document.getElementById('editUsernameForm').style.display = 'block';

	// Focus on the input field - triggers the keyboard cursor automatically in the input field
	document.getElementById('newUsername').focus();
}


/** [5.1.2]
 * A function that is called when the `Save` button is clicked (onclick) and
 * triggers POST form for @update_username route so that backend can retrieve
 * `newUsername` value and store it (or abort it) in the SQL database
 */
function saveNewUsername() {
	return true;
}


/** [5.1.3]
 * A function that is called when the `Cancel` button is clicked (onclick) and
 * hides the text field for the new username (placeholder='Enter new username'),
 * `Save` and `Cancel` buttons. It also erases any given input for the
 * `newUserName` value.
 */
function cancelUsernameEdit() {
	document.getElementById('usernameContainer').style.display = 'block';
	document.getElementById('editUsernameForm').style.display = 'none';
	document.getElementById('newUsername').value = "";
}


/** [5.1.4]
 * A function that is called when `Reset Password` or `Delete Account` buttons are
 * pressed (onclick). It focus the keyboard cursor on the input field when the
 * bootstrap modal is shown to the user.
 */
function cursorFocus(button) {
	var modalId = button.getAttribute('data-modal-id');
	var inputFieldId = button.getAttribute('data-input-field-id');

	document.getElementById(modalId).addEventListener('shown.bs.modal', function () {
		document.getElementById(inputFieldId).focus();
	});
}


/** [5.1.5]
 * A jQuery function that validates realtime the account route form
 */
function jQueryValidateUpdateAccount() {
	jQuery.validator.addMethod("text", function (value, element) {
		var invalidCharactersRegex = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\s]/;
		var result = this.optional(element) ||
			(value.length >= 3 && !invalidCharactersRegex.test(value));
		return result;
	},
		`Username must be at least 3 characters long and cannot contain
		punctuation characters or whitespaces.`
	);

	$("#updateUsernameForm").validate({
		rules:
		{
			newUsername:
			{
				required: true,
				text: true
			}
		},
		messages:
		{
			newUsername:
			{
				required: "This field is required",
			},
		}
	});

	$("#passwordResetForm").validate({
		rules:
		{
			oldPassword:
			{
				required: true
			},
			newPassword:
			{
				required: true
			},
			confirmNewPassword:
			{
				required: true,
				equalTo: "#newPassword"
			}
		},
		messages:
		{
			oldPassword:
			{
				required: "This field is required",
			},
			newPassword:
			{
				required: "This field is required",
			},
			confirmNewPassword: {
				required: "This field is required",
				equalTo: "Please enter the same password as above"
			}
		}
	});

	$("#deleteAccountForm").validate({
		rules:
		{
			deleteAccountConfirmation:
			{
				required: true,
				email: true,
				text: false
			}
		},
		messages:
		{
			deleteAccountConfirmation:
			{
				required: "This field is required",
				email: "Please enter a valid email address"
			},
		}
	});
}


/** [5.1.6]
 * A jQuery function that resets all the modal inputs in case they are
 * closed/hidden. It is called in [5.2].
 */
function resetModalInputs() {
	$(document).ready(function () {
		$('#passwordResetModal').on('hidden.bs.modal', function () {
			$('#oldPassword').val('');
			$('#newPassword').val('');
			$('#confirmNewPassword').val('');
		});
	});

	$(document).ready(function () {
		$('#deleteAccountModal').on('hidden.bs.modal', function () {
			$('#deleteAccountConfirmation').val('');
		});
	});
}


// ----- [5.2] EXECUTES WHEN ACCOUNT ROUTE LOADS -----//
// Execute the following code only for account route
$(document).ready(function () {
	var formIds = [
		"#updateUsernameForm",
		"#passwordResetForm",
		"#deleteAccountForm"
	];

	// Re-execute validation if any of the account route forms is submitted or changed
	formIds.forEach(function (formId) {
		$(formId).on("submit", function () {
			jQueryValidateUpdateAccount();
		});
		$(formId).on("change", function () {
			jQueryValidateUpdateAccount();
		});
	});

	// Initial validation when the page loads
	if (window.location.pathname === '/account') {
		jQueryValidateUpdateAccount();
	}

	// Reset modal inputs if not vissible
	resetModalInputs()
});




/** ||||| [6.0] @index ROUTE ||||| */
// ----- [6.1] UPDATE EXPOSURE -----//
/** [6.1.1]
 * A function that changes the exposure setting with asynchronous logic.
 */
function applyExposureFormListener() {
	$('.exposure-form').off('click').on('click', function (event) {
		event.preventDefault(); // Prevent form submission

		var form = $(this);
		var submissionId = form.data('submission-id');
		var newExposure = form.data('new-exposure');

		$.ajax({
			type: 'POST',
			url: '/update_exposure',
			data: {
				submission_id: submissionId,
				new_exposure: newExposure
			},
			success: function () {
				// Inform user about the updated exposure
				alert('Exposure updated successfully!')

				// Update button appearance
				var button = form.find('button[type="submit"]');
				if (newExposure === 'private') {
					button.removeClass('btn-success').addClass('btn-primary').text('Private');
					form.data('new-exposure', 'public');
				} else {
					button.removeClass('btn-primary').addClass('btn-success').text('Public');
					form.data('new-exposure', 'private');
				}

				// Recall the function to be ready if the user clicks the button again
				applyExposureFormListener();
			},
			error: function (error) {
				// Handle errors if any
				console.error('Error:', error);
				// You can display error messages to the user
			}
		});
	});
}


// ----- [6.2] EXECUTES WHEN INDEX ROUTE LOADS -----//
// Execute the following code only for index route
$(document).ready(function () {
	if (window.location.pathname === '/') {
		// Get exposure button ready to be clicked
		applyExposureFormListener();
	}
});
