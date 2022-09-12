import django
import pytest
from dateutil.parser import parse
from rest_framework.test import APIClient
django.setup()

from core.models import Property, PricingRule


@pytest.fixture
def property_standard():
    return Property(
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
        property=property_standard,
        price_modifier=float(-10),
        min_stay_length=7,
        fixed_price=None,
        specific_day=None
    )


@pytest.fixture
def pricing_rule_2(property_standard):
    return PricingRule(
        property=property_standard,
        price_modifier=float(-20),
        min_stay_length=30,
        fixed_price=None,
        specific_day=None
    )


@pytest.fixture
def pricing_rule_3(property_standard):
    return PricingRule(
        property=property_standard,
        price_modifier=None,
        min_stay_length=None,
        fixed_price=20,
        specific_day=parse('01-04-2022')
    )
