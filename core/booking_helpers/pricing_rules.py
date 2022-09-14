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


def filter_double_condition_rules(rules:list[PricingRule], days_list: DatetimeIndex) -> list[PricingRule]:
    days_list = list(days_list)
    rules = [rule for rule in rules if rule.has_double_condition()]
    rules = [rule for rule in rules if rule.specific_day in days_list]
    return rules

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

    double_condition_rules = [rule for rule in pricing_rules if (rule.specific_day and rule.min_stay_length) in days_list]
    remaining_rules = list(set(pricing_rules) - set(double_condition_rules))
    specific_day_rules = list(filter(lambda rule: rule.specific_day is not None, remaining_rules))
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

    if double_condition_rules:
        double_rules = filter_specific_day_rules(specific_day_rules, days_list)
        if not double_rules:
            return valid_rules

        double_rules = filter_min_stay_rules(min_stay_length_rules, total_days)
        if double_rules:
            for rule in double_rules:
                valid_rules.append(rule)

    return valid_rules

def apply_double_rule(rule, day_list) -> float:
    return float(rule.fixed_price * len(day_list))

def get_booking_prices(days_list: DatetimeIndex, rules_to_apply: list[PricingRule]) -> (float, list, float):

    price_modifier = float()
    special_day_list = list()
    fixed_price = float()

    for rule in rules_to_apply:



        if rule.min_stay_length:
            price_modifier = rule.price_modifier
        if rule.specific_day:
            special_day_list.append(rule.specific_day)
            fixed_price = rule.fixed_price

        # If rule has min_stay_length , it means both conditions need to be true.
        if rule.has_double_condition():
            return apply_double_rule(rule, days_list)

        # If a rule has a price_modifier and a fixed_price, fixed_price should be used.
        # If this rule is min_stay_length, this means that is TOP priority?
        if rule.fixed_price and rule.price_modifier:
            rule.price_modifier = None
            if rule.min_stay_length:
                return apply_double_rule(rule, days_list)
            fixed_price = rule.fixed_price

    return price_modifier, special_day_list, fixed_price


def apply_rules(days_list: DatetimeIndex, base_price: float, rules_to_apply: list[PricingRule]) -> float:
    """Apply the appropriate rule for each day.
    Args:
        days_list: List of all dates to be booked.
        rules_to_apply: List of PricingRules selected to be applied
        base_price: The base_price of the Property to be booked.
    Returns:
        The sum of all charges for every day.
    """
    total = list()


    price_modifier, special_day_list, fixed_price = get_booking_prices(days_list, rules_to_apply)
    for day in days_list:
        if day in special_day_list:
            total.append(fixed_price)
        else:
            total.append(base_price - ((base_price / 100) * abs(price_modifier)))

    return float(sum(total))
