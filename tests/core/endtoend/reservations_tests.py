import json
from typing import Union

import pytest
from rest_framework.test import APIClient

from core.models import PricingRule, RentalProperty

Fixture = Union


@pytest.mark.django_db
class TestBookingEndpoints:
    booking_endpoint = '/api/booking/'
    client = APIClient()

    @pytest.mark.django_db
    def test_case_1(self, property_standard: Fixture[RentalProperty], pricing_rule_1: Fixture[PricingRule]):
        """
        # Case 1:
            - Property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-10-2022
                - stay length: 10 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
            - Final price: 90

        # Test:
            . Integration is OK.
			. Total days of the booking is correct.
            . Min_stay_rule is recorganized and propperly applied.
            . Final price is correct.

        """

        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_1.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 90
        assert response_content.get('final_price') == expected_final_price


    @pytest.mark.django_db
    def test_case_2(self, property_standard: Fixture[RentalProperty], pricing_rule_1: Fixture[PricingRule],
                    pricing_rule_2: Fixture[PricingRule]):
        """
        # Case 2:
            - rental_property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-10-2022
                - stay length: 10 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
                2- min_stay_length: 30, price_modifier: -20
            - Final price: 90

        # Test:
            . If multiple rules with min_stay_length, the bigger applying min_stay_length should be selected

        """
        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_1.save()
        pricing_rule_2.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 90
        assert response_content.get('final_price') == expected_final_price

    @pytest.mark.django_db
    def test_case_3(self, property_standard: Fixture[RentalProperty], pricing_rule_1: Fixture[PricingRule],
                    pricing_rule_3: Fixture[PricingRule]):
        """
        # Case 3:
            - rental_property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-10-2022
                - stay length: 10 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
                2- specific_day: 01-04-2022, fixed_price: 20
            - Final price: 101

        # Test.
            . Specific day rule is recorganized and propperly applied.
		    . Interaction between rules and proper selection.
		    . Min  stay length is applied even if a specific day is between.
            .  A specific_day rule has more priority than min_stay_length rules.
        """
        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_1.save()
        pricing_rule_3.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 101
        assert response_content.get('final_price') == expected_final_price

    @pytest.mark.django_db
    def test_case_4(self, property_standard: Fixture[RentalProperty], pricing_rule_1: Fixture[PricingRule],
                    pricing_rule_3: Fixture[PricingRule]):
        """
                ## Case 4:
            - rental_property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-7-2022
                - stay length: 7 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
                2- specific_day: 01-04-2022, fixed_price: 20

                        expected_final_price = 74

        """
        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_1.save()
        pricing_rule_3.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-7-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 74
        assert response_content.get('final_price') == expected_final_price

    @pytest.mark.django_db
    def test_case_5(self, property_standard: Fixture[RentalProperty], pricing_rule_1: Fixture[PricingRule],
                    pricing_rule_4: Fixture[PricingRule]):
        """
                ## Case 5:

            - rental_property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-7-2022
                - stay length: 7 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
                2- specific_day: 01-04-2022, price_modifier: 10

        expected_final_price = 80


        """
        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_1.save()
        pricing_rule_4.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-7-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 65
        assert response_content.get('final_price') == expected_final_price

    @pytest.mark.django_db
    def test_case_6(self, property_standard: Fixture[RentalProperty], pricing_rule_5: Fixture[PricingRule],
                    pricing_rule_3: Fixture[PricingRule], pricing_rule_1: Fixture[PricingRule]):
        """
        # Case 6:-
            - rental_property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-10-2022
                - stay length: 10 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
                2- min_stay_length: 7, price_modifier: -10, specific_day: 01-05-2022, fixed_price: 5
                3- specific_day: 01-04-2022, fixed_price: 20
            - Final_price = 70.0
        # Test:
            .  If a rule has both conditions, it means both conditions need to be true.
        """
        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_5.save()
        pricing_rule_3.save()
        pricing_rule_1.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-7-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 70.0
        assert response_content.get('final_price') == expected_final_price

    @pytest.mark.django_db
    def test_case_7(self, property_standard: Fixture[RentalProperty], pricing_rule_1: Fixture[PricingRule],
                    pricing_rule_7: Fixture[PricingRule]):
        """
        # Case 7:
            - rental_property base_price = 10
                - Booking:
                    - date_start: 01-01-2022
                    - date_end: 01-10-2022
                    - stay length: 10 days
                - Pricing Rules
                    1- min_stay_length: 7, price_modifier: -10
                    2- min_stay_length: 7, price_modifier: -20
                - Final price:
                        expected_final_price = 80.0
        # Test:
            . If multiples min_stay_length rule, select the one with biggest discount.

        """
        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_1.save()
        pricing_rule_7.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 80.0
        assert response_content.get('final_price') == expected_final_price


    @pytest.mark.django_db
    def test_case_9(self, property_standard: Fixture[RentalProperty], pricing_rule_3: Fixture[PricingRule],
                    pricing_rule_8: Fixture[PricingRule]):
        """
                ## Case 9:
            - rental_property base_price = 10
                - Booking:
                    - date_start: 01-01-2022
                    - date_end: 01-10-2022
                    - stay length: 10 days
                - Pricing Rules
                    2- specific_day: 01-04-2022, fixed_price: 20

                    2- specific_day: 01-05-2022, price_modifier: 30

                - Final price:

                        expected_final_price = 130.0

        """
        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_3.save()
        pricing_rule_8.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 130.0
        assert response_content.get('final_price') == expected_final_price

    @pytest.mark.django_db
    def test_case_10(self, property_standard: Fixture[RentalProperty], pricing_rule_1: Fixture[PricingRule],
                     pricing_rule_9: Fixture[PricingRule]):
        """
        # Case 10:
            - rental_property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-10-2022
                - stay length: 10 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
                2- min_stay_length: 8, price_modifier: -20
            - Final price: 80.0

        # Test:
            . If multiples specific_day rule, select the one with biggest discount.
        """
        # Set the rental_property and Rules
        property_standard.save()
        pricing_rule_1.save()
        pricing_rule_9.save()

        # Create the reservation
        url = self.booking_endpoint
        response = self.client.post(url, {"rental_property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 80.0
        assert response_content.get('final_price') == expected_final_price
