import re


def func_to_valid_serializer(value):
    return value


def validate_agricultural_year_period(value):
    regex = '[0-9]{2}/[0-9]{2}'
    return re.findall(regex, value)
