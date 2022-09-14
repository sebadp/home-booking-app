Southern Code Django challenge

This project is the resolution for the Southern Code Django challenge by Sebastián Dávila.

# Requirements questions:
###
- If it has both(same rule a contition of min_stay_length and specific_day), it means both conditions need to be true.
- In this case should we charge the fixed price for each day?
###
- If a rule has a price_modifier and a fixed_price, fixed_price should be used.
- If this rule is min_stay_length, this means that is TOP priority?

# Branches and tasks solved:

### SCDCM-1/crud_endpoints
- Using django-rest-framework, create CRUD endpoints to interact with the 3 models.

### SCDCM-2/add_filters
- For Property and Booking, create some basic filters for the list endpoint using django-filters

### SCDCM-3/add_required_test_cases
- Add Tests, specially for the pricing rules calculation. At least the 3 cases described in this file should be covered.

### SCDCM-4/implement_reservation_logic
- Feel free to modify the models, but the main focus of this test is the pricing rules calculation.

### SCDCM-5/add_docstrings_and_type_hinting
- Extra points for docstrings, type hinting and return types!

### SCDCM-6/clean_up_project
- Please deploy the backend server in heroku or any similar free service
- Extra points for a dockerized solution!

# Deployed at Heroku:
- URL: https://rocky-reaches-56968.herokuapp.com/





