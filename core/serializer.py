from .models import PricingRule, RentalProperty, Booking
from rest_framework import serializers


class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRule
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalProperty
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
