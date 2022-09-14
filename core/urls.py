from django.urls import path
from core.views import PricingRuleListView, PricingRuleDetailView, PropertyListView, PropertyDetailView, BookingListView, BookingDetailView

urlpatterns = [
    path('pricing-rule/', PricingRuleListView.as_view()),
    path('pricing-rule/<int:pk>', PricingRuleDetailView.as_view()),
    path('property/', PropertyListView.as_view()),
    path('property/<int:pk>', PropertyDetailView.as_view()),
    path('booking/', BookingListView.as_view()),
    path('booking/<int:pk>', BookingDetailView.as_view())
]
