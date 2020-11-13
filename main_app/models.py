import re

from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

WEEKDAYS = ["monday", "tuesday", "wednesday",
            "thursday", "friday", "saturday", "sunday"]
DEFAULT_OPENING_TIME = '09:00'
DEFAULT_CLOSING_TIME = '17:00'

class OpeningHours(object):
    def __init__(self, enabled, opening_time, closing_time):
        self.enabled = enabled
        self.opening_time = opening_time
        self.closing_time = closing_time


class WeeklyOpeningHours(object):
    def __init__(self, opening_hours_array):
        self.opening_hours = {}
        for i in range(len(WEEKDAYS)):
            self.opening_hours[WEEKDAYS[i]] = opening_hours_array[i]


def parse_weekly_opening_hours(value):
    opening_hours = []
    for weekday in WEEKDAYS:
        match = re.search(
            '%s ([0-9][0-9]:[0-9][0-9]) ([0-9][0-9]:[0-9][0-9])' % weekday, value)
        if match:
            opening_hours.append(OpeningHours(
                True, match.group(1), match.group(2)))
        else:
            opening_hours.append(OpeningHours(False, DEFAULT_OPENING_TIME, DEFAULT_CLOSING_TIME))
    return WeeklyOpeningHours(opening_hours)


class WeeklyOpeningHoursField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 512
        kwargs['default'] = ''
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'char(512)'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return parse_weekly_opening_hours(value)

    def to_python(self, value):
        if isinstance(value, WeeklyOpeningHours):
            return value
        if value is None:
            return value
        return parse_weekly_opening_hours(value)

    def get_prep_value(self, value):
        if isinstance(value, str):
            return value
        if value is None:
            return None
        opening_hours_str_list = []
        for weekday in WEEKDAYS:
            if value.opening_hours[weekday].enabled:
                opening_hours_str_list.append('%s %s %s' % (weekday,
                                                            value.opening_hours[weekday].opening_time,
                                                            value.opening_hours[weekday].closing_time))
        return ''.join(opening_hours_str_list)

    def get_db_prep_value(self, value, connection, prepared=False):
        value = super().get_db_prep_value(value, connection, prepared)
        if isinstance(value, str):
            return value
        if value is None:
            return ""
        opening_hours_str_list = []
        for weekday in WEEKDAYS:
            if value.opening_hours[weekday].enabled:
                opening_hours_str_list.append('%s %s %s' % (value.opening_hours[weekday].opening_time,
                                                            value.opening_hours[weekday].closing_time))
        return ''.join(opening_hours_str_list)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.CharField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Resource(models.Model):
    # constants for the enum field, category.
    UNKNOWN = "UNKNOWN"
    FOOD = "FOOD"
    CLOTHING = "CLOTHING"
    ADDICTION_RECOVERY = "ADDICTION_RECOVERY"
    HYGIENE = "HYGIENE"
    FINANCIAL_EMPOWERMENT = "FINANCIAL_EMPOWERMENT"
    SHELTER = "SHELTER"
    WOMEN_AND_CHILDREN = "WOMEN_AND_CHILDREN"
    MENTAL_HEALTH_SERVICES = "MENTAL_HEALTH_SERVICES"
    FINANCIAL_EMPOWERMENT = "FINANCIAL_EMPOWERMENT"
    MEDICAL_ASSISTANCE = "MEDICAL_ASSISTANCE"

    CATEGORIES = (
        (UNKNOWN, "Unknown"),
        (FOOD, "Food"),
        (CLOTHING, "Clothing"),
        (ADDICTION_RECOVERY, "Addiction Recovery"),
        (HYGIENE, "Hygiene"),
        (FINANCIAL_EMPOWERMENT, "Financial Empowerment"),
        (SHELTER, "Shelter"),
        (WOMEN_AND_CHILDREN, "Women and Children"),
        (MENTAL_HEALTH_SERVICES, "Mental Health Services"),
        (FINANCIAL_EMPOWERMENT, "Financial Empowerment"),
        (MEDICAL_ASSISTANCE, "Medical Assistance")
    )

    resource_name = models.CharField(max_length=100)
    # TODO: org_name can be a ForeignKey.
    org_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100,
                                choices=CATEGORIES,
                                default=UNKNOWN)

    opening_hours = WeeklyOpeningHoursField()
    address = models.CharField(max_length=100, blank=True)
    street_number = models.CharField(max_length=100, blank=True)
    street_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    long = models.DecimalField(max_digits=64, decimal_places=32)
    lat = models.DecimalField(max_digits=64, decimal_places=32)
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, blank=True)
    notes = models.TextField(max_length=250, blank=True)

    ordering = ['org_name', 'category', 'resource_name']

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        return f'{self.org_name}: {self.resource_name}'
