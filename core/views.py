import pandas as pd
from dateutil import parser
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializer import PropertySerializer, PricingRuleSerializer, BookingSerializer
from .booking_helpers.availability import check_availability, check_reservation_is_valid
from .booking_helpers.pricing_rules import get_rules_to_apply, apply_rules
from .models import PricingRule, Property, Booking


class PropertyListView(generics.ListCreateAPIView):
    """
    List all Propertys, or create a new Property.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('id', 'name')


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Property instance.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PricingRuleListView(generics.ListCreateAPIView):
    """
    List all PricingRules, or create a new PricingRule.
    """
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer


class PricingRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet PricingRule.
    """
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer


class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a Booking instance.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


@api_view(['GET', 'POST'])
def get_post_booking_view(request):
    """
    :[POST]:
        Description: List all Bookings

    :[GET]:
        Description: Create a new Booking.
        Summary:
            . Check the Booking is valid. Handle Exception.
            . Check availability of time_slots for the Booking. Handle Exception.
            . Select the PricingRules to aplly according to requirements.
            . Apply the selected PricingRules and apply to each day.
        Responses:
            '200':
                Description: Booking item successfully created.
            '400':
                Description: Bad Request.

    """


    if request.method == 'GET':
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        valid_reservation = check_reservation_is_valid(request.data)
        if not valid_reservation:
            # TODO: HANDLE THIS!
            pass

        available_time_slot = check_availability(request.data)

        if not available_time_slot:
            # TODO: HANDLE THIS!
            pass

        selected_property = Property.objects.get(pk=request.data.get('property'))
        property_pricing_rules = PricingRule.objects.filter(property=selected_property.id)

        days_list = pd.date_range(request.data.get('date_start'), request.data.get('date_end'))

        rules_to_apply = get_rules_to_apply(days_list, property_pricing_rules)

        if not rules_to_apply:
            final_price = float(len(days_list) * selected_property.base_price)
        else:
            final_price = apply_rules(days_list, rules_to_apply, selected_property.base_price)

        data = {
            "property": request.data.get('property'),
            "date_start": parser.parse(request.data.get('date_start')).date(),
            "date_end": parser.parse(request.data.get('date_end')).date(),
            "final_price": final_price
        }
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
