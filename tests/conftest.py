import django
import pytest
from dateutil.parser import parse
from rest_framework.test import APIClient
django.setup()

from core.models import RentalProperty, PricingRule

from django.core.management import call_command



@pytest.fixture
def property_standard():
    return RentalProperty(
        id=1,
        name='Standard',
        base_price=10
    )


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def pricing_rule_1(property_standard):
    return PricingRule(
        rental_property=property_standard,
        price_modifier=float(-10),
        min_stay_length=7,
        fixed_price=None,
        specific_day=None
    )


@pytest.fixture
def pricing_rule_2(property_standard):
    return PricingRule(
        rental_property=property_standard,
        price_modifier=float(-20),
        min_stay_length=30,
        fixed_price=None,
        specific_day=None
    )


@pytest.fixture
def pricing_rule_3(property_standard):
    return PricingRule(
        rental_property=property_standard,
        price_modifier=None,
        min_stay_length=None,
        fixed_price=20,
        specific_day=parse('01-04-2022')
    )

@pytest.fixture
def pricing_rule_4(property_standard):
    return PricingRule(
        rental_property=property_standard,
        price_modifier=10,
        min_stay_length=None,
        fixed_price=None,
        specific_day=parse('01-04-2022')
    )

@pytest.fixture
def pricing_rule_5(property_standard):
    return PricingRule(
        rental_property=property_standard,
        price_modifier=-10,
        min_stay_length=7,
        fixed_price=5,
        specific_day=parse('01-05-2022')
    )

@pytest.fixture
def pricing_rule_7(property_standard):
    return PricingRule(
        rental_property=property_standard,
        price_modifier=float(-20),
        min_stay_length=7,
        fixed_price=None,
        specific_day=None
    )

@pytest.fixture
def pricing_rule_8(property_standard):
    return PricingRule(
        rental_property=property_standard,
        price_modifier=None,
        min_stay_length=None,
        fixed_price=30,
        specific_day=parse('01-05-2022')
    )

@pytest.fixture
def pricing_rule_9(property_standard):
    return PricingRule(
        rental_property=property_standard,
        price_modifier=float(-20),
        min_stay_length=8,
        fixed_price=None,
        specific_day=None
    )
