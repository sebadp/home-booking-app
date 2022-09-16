from itertools import groupby
from typing import Tuple, List

from pandas import DatetimeIndex

from core.models import PricingRule


def filter_from_similar_rules(rules: list[PricingRule]) -> list[PricingRule]:
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


def process_min_stay_length_rule(min_stay_length_rules: list[PricingRule], total_days: int,
                                 valid_rules: list[PricingRule]) -> list[PricingRule]:
    """ Select the Min Stay Length rule that has priority.
    Args:
        total_days: total days to be booked.
        min_stay_length_rules: List of PricingRules to be processed.
        valid_rules: List of valid rules according to booking request, placeholder for the new valid rules.
    Returns:
        valid_rules: List of PricingRules to be processed.
    """
    if min_stay_length_rules:
        rules = list(filter(lambda rule: rule.min_stay_length < total_days, min_stay_length_rules))
        rules = filter_from_similar_rules(rules)
        filtered_rule = max(rules, key=lambda rule: rule.min_stay_length)
        if filtered_rule:
            valid_rules.append(filtered_rule)
    return valid_rules


def process_specific_day_rule(days_list: DatetimeIndex, specific_day_rules: list[PricingRule],
                              valid_rules: list[PricingRule]) -> list[PricingRule]:
    """ Select the specific_day rule that has priority.
    Args:
        days_list: DatetimeIndex of all dates to be booked.
        specific_day_rules: List of PricingRules to be processed.
        valid_rules: List of valid rules according to booking request, placeholder for the new valid rules.
    Returns:
        valid_rules: List of PricingRules to be processed.

    """
    days_list = list(days_list)

    if specific_day_rules:
        rules = [rule for rule in specific_day_rules if rule.specific_day in days_list]
        filtered_rules = filter_from_similar_rules(rules)
        if filtered_rules:
            for rule in filtered_rules:
                valid_rules.append(rule)
    return valid_rules


def process_double_condition_rules(days_list: DatetimeIndex, double_condition_rules: list[PricingRule],
                                   valid_rules: list[PricingRule]) -> list[PricingRule]:
    """ Select the specific_day rule that has priority.
    Args:
        days_list: DatetimeIndex of all dates to be booked.
        double_condition_rules: List of PricingRules to be processed.
        valid_rules: List of valid rules according to booking request, placeholder for the new valid rules.
    Returns:
        valid_rules: List of PricingRules to be processed.

    """
    total_days = len(days_list)
    rules = list(filter(lambda rule: rule.min_stay_length < total_days, double_condition_rules))
    rules = filter_from_similar_rules(rules)
    double_rule = max(rules, key=lambda rule: rule.min_stay_length)

    if double_rule:
        valid_rules.append(double_rule)
    return valid_rules


def identify_rules(days_list: DatetimeIndex, pricing_rules: list[PricingRule]) -> Tuple[list[PricingRule], list[PricingRule], list[PricingRule]]:
    """
    Args:
        days_list: DatetimeIndex of all dates to be booked.
        pricing_rules: List of PricingRules to be filtered.
    Returns:
        double_condition_rules
        min_stay_length_rules
        specific_day_rules

    """
    double_condition_rules = [rule for rule in pricing_rules if rule.min_stay_length
                              and (rule.specific_day in days_list)]
    remaining_rules = list(set(pricing_rules) - set(double_condition_rules))
    specific_day_rules = list(filter(lambda rule: rule.specific_day is not None, remaining_rules))
    min_stay_length_rules = list(set(pricing_rules) - set(specific_day_rules))
    return double_condition_rules, min_stay_length_rules, specific_day_rules


def get_rules_to_apply(days_list: DatetimeIndex, pricing_rules: list[PricingRule]) -> list[PricingRule]:
    """Select the Pricing Rules that are relevant to apply for each day. More info at: README.md:MOST RELEVANT RULE
    Args:
        days_list: DatetimeIndex of all dates to be booked.
        pricing_rules: List of PricingRules to be filtered.
    Returns:
        List of PricingRules selected to be applied.
    """
    valid_rules: List = list()
    total_days = len(days_list)

    double_condition_rules, min_stay_length_rules, specific_day_rules = identify_rules(days_list, pricing_rules)

    valid_rules = process_specific_day_rule(days_list, specific_day_rules, valid_rules)

    valid_rules = process_min_stay_length_rule(min_stay_length_rules, total_days, valid_rules)

    valid_rules = process_double_condition_rules(days_list, specific_day_rules, valid_rules)

    return valid_rules


def apply_double_rule(fixed_price: float, day_list) -> float:
    """
    Args:

    Returns:
        The sum of all charges for every day.
    """
    return float(fixed_price * len(day_list))


def get_booking_prices(rules_to_apply: list[PricingRule]) -> Tuple[float, list, float, bool]:
    """
    Args:

    Returns:
        price_modifier:
        special_day_list:
        fixed_price:
        double_rule:
    """
    price_modifier = float()
    special_day_list = list()
    fixed_price = float()
    double_rule: bool = False
    for rule in rules_to_apply:
        if rule.min_stay_length:
            price_modifier = rule.price_modifier
        if rule.specific_day:
            special_day_list.append(rule.specific_day)
            fixed_price = rule.fixed_price

        # If rule has min_stay_length , it means both conditions need to be true.
        if rule.has_double_condition():
            double_rule = True
            return price_modifier, special_day_list, fixed_price, double_rule

        # If a rule has a price_modifier and a fixed_price, fixed_price should be used.
        # If this rule is min_stay_length, this means that is TOP priority?
        if rule.fixed_price and rule.price_modifier:
            rule.price_modifier = None
            if rule.min_stay_length:
                double_rule = True
                return price_modifier, special_day_list, fixed_price, double_rule
            fixed_price = rule.fixed_price

    return price_modifier, special_day_list, fixed_price, double_rule


def apply_rules(days_list: DatetimeIndex, base_price: float, rules_to_apply: list[PricingRule]) -> float:
    """Apply the appropriate rule for each day.
    Args:
        days_list: DatetimeIndex of all dates to be booked.
        rules_to_apply: List of PricingRules selected to be applied
        base_price: The base_price of the Property to be booked.
    Returns:
        The sum of all charges for every day.
    """
    total = list()

    price_modifier, special_day_list, fixed_price, double_rule = get_booking_prices(rules_to_apply)
    if double_rule:
        apply_double_rule(fixed_price, days_list)
    for day in days_list:
        if day in special_day_list:
            total.append(fixed_price)
        else:
            total.append(base_price - ((base_price / 100) * abs(price_modifier)))

    return float(sum(total))
