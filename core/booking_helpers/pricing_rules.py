from itertools import groupby
from pandas import DatetimeIndex

from core.models import PricingRule


def filter_from_similar_rules(rules:list[PricingRule]) -> list[PricingRule]:
    """Select the rules with the biggest price_modifier or fixed_price.
    Args:
        rules: List of PricingRules to be filtered.
    Returns:
        List of PricingRules filtered.
    """
    groups = []
    uniquekeys = []
    key_func = lambda x: x.get_key_field
    for k, g in groupby(rules, key_func):
        groups.append(list(g))  # Store group iterator as a list
        uniquekeys.append(k)
    min_stay_length_rules = list()
    for group in groups:
        if len(group) > 1:
            min_stay_length_rules.append(max(group, key=key_func))
        min_stay_length_rules.append(group[0])
    return min_stay_length_rules


def filter_specific_day_rules(rules:list[PricingRule], days_list: DatetimeIndex) -> list[PricingRule]:
    """Select Specific Day rules that include a rule at the booking days_list.
       Select rules with priority.
    Args:
        rules: List of PricingRules to be filtered.
        days_list: List of all dates to be booked.
    Returns:
        List of PricingRules filtered.
    """
    days_list = list(days_list)
    rules = [rule for rule in rules if rule.specific_day in days_list]
    rules = filter_from_similar_rules(rules)
    return rules


def filter_min_stay_rules(rules:list[PricingRule], total_days: int) -> list[PricingRule]:
    """Select the Min Stay Length rule that has priority.
    Args:
        rules: List of PricingRules to be filtered.
        total_days: The sum of all days to be booked.
    Returns:
        List of PricingRules filtered.
    """

    rules = list(filter(lambda rule: rule.min_stay_length < total_days, rules))
    rules = filter_from_similar_rules(rules)

    rules = max(rules, key=lambda rule: rule.min_stay_length)

    return rules


def get_rules_to_apply(days_list: DatetimeIndex, pricing_rules:list[PricingRule]) -> list[PricingRule]:
    """Select the Pricing Rules that are relevant to apply for each day. More info at: README.md:MOST RELEVANT RULE
    Args:
        days_list: List of all dates to be booked.
        pricing_rules: List of PricingRules to be filtered.
    Returns:
        List of PricingRules selected to be applied.
    """
    valid_rules = []
    total_days = len(days_list)
    specific_day_rules = list(filter(lambda rule: rule.specific_day is not None, pricing_rules))
    min_stay_length_rules = list(set(pricing_rules) - set(specific_day_rules))

    if specific_day_rules:
        filtered_rules = filter_specific_day_rules(specific_day_rules, days_list)
        if filtered_rules:
            for rule in filtered_rules:
                valid_rules.append(rule)

    if min_stay_length_rules:
        filtered_rules = filter_min_stay_rules(min_stay_length_rules, total_days)
        if filtered_rules:
            valid_rules.append(filtered_rules)

    return valid_rules


def apply_rules(days_list: DatetimeIndex, rules_to_apply: list[PricingRule], base_price:float) -> float:
    """Apply the appropriate rule for each day.
    Args:
        days_list: List of all dates to be booked.
        rules_to_apply: List of PricingRules selected to be applied
        base_price: The base_price of the Property to be booked.
    Returns:
        The sum of all charges for every day.
    """
    total = list()
    price_modifier = float()
    special_day_list = list()
    fixed_price = float()
    for rule in rules_to_apply:
        if rule.min_stay_length:
            price_modifier = rule.price_modifier
        if rule.specific_day:
            special_day_list.append(rule.specific_day)
            fixed_price = rule.fixed_price
    for day in days_list:
        if day in special_day_list:
            total.append(fixed_price)
        else:
            total.append(base_price - ((base_price / 100) * abs(price_modifier)))

    return float(sum(total))
