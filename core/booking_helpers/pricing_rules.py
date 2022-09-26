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
    key_func = lambda x: x.get_key_field

    for _, g in groupby(rules, key_func):
        groups.append(list(g))  # Store group iterator as a list

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
        rules = list(filter(lambda rule: rule.min_stay_length <= total_days, min_stay_length_rules))
        rules = filter_from_similar_rules(rules=rules)
        if rules:
            filtered_rule = max(rules, key=lambda rule: abs(rule.price_modifier))
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
    days_list = [day.date() for day in days_list]

    if specific_day_rules:
        rules = [rule for rule in specific_day_rules if rule.specific_day in days_list]
        filtered_rules = filter_from_similar_rules(rules=rules)
        if filtered_rules:
            for rule in filtered_rules:
                valid_rules.append(rule)
    return valid_rules


def identify_rules(pricing_rules: list[PricingRule]) -> Tuple[list[PricingRule], list[PricingRule]]:
    """
    Args:
        pricing_rules: List of PricingRules to be filtered.
    Returns:
        min_stay_length_rules
        specific_day_rules

    """

    min_stay_length_rules = list(filter(lambda rule: rule.min_stay_length is not None, pricing_rules))
    specific_day_rules = list(set(pricing_rules) - set(min_stay_length_rules))

    return min_stay_length_rules, specific_day_rules


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

    min_stay_length_rules, specific_day_rules = identify_rules(pricing_rules=pricing_rules)

    valid_rules = process_specific_day_rule(days_list=days_list, specific_day_rules=specific_day_rules,
                                            valid_rules=valid_rules)

    valid_rules = process_min_stay_length_rule(min_stay_length_rules=min_stay_length_rules, total_days=total_days,
                                               valid_rules=valid_rules)

    return valid_rules


def get_booking_prices(rules_to_apply: list[PricingRule]) -> Tuple[float, dict]:
    """
    Args:
        rules_to_apply: List of PricingRules to be filtered.
    Returns:
        price_modifier: Final price modifier to be applied.
        special_day_list: List of all days to be charged as special day.
    """
    price_modifier = float()
    special_day_dict = dict()

    for rule in rules_to_apply:
        if rule.min_stay_length:
            price_modifier = rule.price_modifier
        if rule.specific_day:
            special_day_dict[rule.specific_day] = rule

    return price_modifier, special_day_dict


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

    price_modifier, special_day_dict = get_booking_prices(rules_to_apply=rules_to_apply)

    for day in days_list:

        if day.date() in special_day_dict.keys():
            rule = special_day_dict[day.date()]
            if rule.fixed_price:

                total.append(rule.fixed_price)
            else:
                total.append(base_price + ((base_price / 100) * rule.price_modifier))
        else:
            total.append(base_price + ((base_price / 100) * price_modifier))
    return float(sum(total))
