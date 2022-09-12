Southern Code Django challenge

This project represents a real life API which is used for listing and booking properties.

We have some reduced versions of the models that the real app uses:
    - Property: A house, flat, hotel room, cabin, etc.
    - Booking: A property booked for a range of dates. In this case it also is in charge of storing the final price.
    - PricingRule: It can be a percent modifier or a fixed price. More information bellow.

# Important Notes:
- Dates are in the following format: “mm-dd-yyyy”
- This is the first version of the code challenge. If you believe something is wrong or not clear enough, feel free to contact alexisgiovoglanian@southerncode.us or the recruiting team.


# Tasks:
SCDCM-1/crud_endpoints
- Using django-rest-framework, create CRUD endpoints to interact with the 3 models.

- For Property and Booking, create some basic filters for the list endpoint using django-filters
- Add Tests, specially for the pricing rules calculation. At least the 3 cases described in this file should be covered.
- Feel free to modify the models, but the main focus of this test is the pricing rules calculation.
- Please deploy the backend server in heroku or any similar free service
- Extra points for a dockerized solution!
- Extra points for docstrings, type hinting and return types!


# Pricing Rule:
- A pricing rule is dynamically applied to a property.
- It can be a positive percent modifier (increment), negative (discount) or a fixed price.
- Pricing rules need to be checked for every day of the booking dates.
- It is possible that multiple rules apply for the same date, but only the most relevant rule should be selected. 
(More information in the section: #Most relevant rule)

# Types of rules:
- If the rule has a minimum stay length to apply, it means the booking stay length needs to be bigger or equal than that for it to apply.
- If the rule has a specific date, it means the rule only applies to that particular day. 
    EX: A booking stay is from 12/20/2021 to 12/31/2021, and we have a rule for 12/24, this rule only applies to the 12/24 day.
- If it has both, it means both conditions need to be true.
- If a rule has a price_modifier and a fixed_price, fixed_price should be used.

# Most relevant rule:
- A specific_day rule has more priority than min_stay_length rules.
- If there are multiple rules with the same min_stay_length or specific_day, the one with the biggest price_modifier or fixed_price is selected.
- If there are multiple rules with min_stay_length, the bigger applying min_stay_length should be selected

# Some cases:
## Case 1:
In this case the base price of the property is 10.
The booking will be 10 days long.
There is a rule that indicates for stays bigger than 7 days, a 10% discount should be applied.
The final price should be 10 days * 10 base_price, minus a 10% discount => 90

    - Property base_price = 10
    - Booking:
        - date_start: 01-01-2022
        - date_end: 01-10-2022
        - stay length: 10 days
    - Pricing Rules
        1- min_stay_length: 7, price_modifier: -10

    - Final price: 90        
    

## Case 2:
In this case the base price of the property is 10.
The booking will be 10 days long.
There is a rule that indicates for stays bigger than 7 days, a 10% discount should be applied.
There is a second rule for stays bigger than 30 days, that rule should not apply, since the stay length is less than 30
The final price should be 10 days * 10 base_price, minus a 10% discount => 90

    - Property base_price = 10
    - Booking:
        - date_start: 01-01-2022
        - date_end: 01-10-2022
        - stay length: 10 days
    - Pricing Rules
        1- min_stay_length: 7, price_modifier: -10
        2- min_stay_length: 30, price_modifier: -20

    - Final price: 90        
    

## Case 3:
In this case the base price of the property is 10.
The booking will be 10 days long.
There is a rule that indicates for stays bigger than 7 days, a 10% discount should be applied.
There is also a rule for 01-04-2022 with a fixed price of 20
In this case the calculation is different, we have a rule that applies to a single day, and it is more important than other rules:

1- The total stay length is bigger than 7, so rule 1 applies, but not to every day.
2- For days 01 to 03, we apply rule 1. (price is 9 * 3 days) => 27
3- For day 04, we apply rule 2 => 20
4- For days 05 to 10, we apply rule 1: (price is 9 * 6 days) => 54
5- Total price is = 101


    - Property base_price = 10
    - Booking:
        - date_start: 01-01-2022
        - date_end: 01-10-2022
        - stay length: 10 days
    - Pricing Rules
        1- min_stay_length: 7, price_modifier: -10
        2- specific_day: 01-04-2022, fixed_price: 20

    - Final price: 101     


