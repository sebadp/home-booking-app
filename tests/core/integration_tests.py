import json
from typing import Union

from core.models import PricingRule, Property, Booking
Fixture = Union


class TestBookingEndpoints:
    booking_endpoint = '/api/booking/'

    def test_case_1(self, api_client, property_standard: Fixture[Property], pricing_rule_1: Fixture[PricingRule]):
        """
                ## Case 1:
            - Property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-10-2022
                - stay length: 10 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
            - Final price: 90
        """
        # Clean DB
        Property.objects.all().delete()
        PricingRule.objects.all().delete()
        Booking.objects.all().delete()

        # Set the Property and Rules
        property_standard.save()
        pricing_rule_1.save()

        # Create the reservation
        client = api_client()
        url = self.booking_endpoint
        response = client.post(url, {"property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 90
        assert response_content.get('final_price') == expected_final_price

    def test_case_2(self, api_client, property_standard: Fixture[Property], pricing_rule_1: Fixture[PricingRule], pricing_rule_2: Fixture[PricingRule]):
        """
                        ## Case 2:
            - Property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-10-2022
                - stay length: 10 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
                2- min_stay_length: 30, price_modifier: -20
            - Final price: 90
        """
        # Clean DB
        Property.objects.all().delete()
        PricingRule.objects.all().delete()

        # Set the Property and Rules
        property_standard.save()
        pricing_rule_1.save()
        pricing_rule_2.save()

        # Create the reservation
        client = api_client()
        url = self.booking_endpoint
        response = client.post(url, {"property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 90
        assert response_content.get('final_price') == expected_final_price

    def test_case_3(self, api_client, property_standard: Fixture[Property], pricing_rule_1: Fixture[PricingRule], pricing_rule_3: Fixture[PricingRule]):
        """
                ## Case 3:
            - Property base_price = 10
            - Booking:
                - date_start: 01-01-2022
                - date_end: 01-10-2022
                - stay length: 10 days
            - Pricing Rules
                1- min_stay_length: 7, price_modifier: -10
                2- specific_day: 01-04-2022, fixed_price: 20
            - Final price: 101
        """
        # Clean DB
        Property.objects.all().delete()
        PricingRule.objects.all().delete()

        # Set the Property and Rules
        property_standard.save()
        pricing_rule_1.save()
        pricing_rule_3.save()

        # Create the reservation
        client = api_client()
        url = self.booking_endpoint
        response = client.post(url, {"property": 1, "date_start": "01-01-2022", "date_end": "01-10-2022"})

        response_content = json.loads(response.content)
        expected_final_price = 101
        assert response_content.get('final_price') == expected_final_price
