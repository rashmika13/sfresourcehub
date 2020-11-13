import re

from .models import OpeningHours
from .models import Resource
from .models import DEFAULT_CLOSING_TIME
from .models import DEFAULT_OPENING_TIME
from .models import WEEKDAYS
from .models import WeeklyOpeningHours
from .models import parse_weekly_opening_hours
from django import forms

class USPhoneNumberMultiWidget(forms.MultiWidget):
    """
    A Widget that splits US Phone number input into three  boxes.
    """
    def __init__(self,attrs=None):
        self.template_name = 'widgets/phone_number.html'
        widgets = [
            forms.TextInput(attrs={'size':'3','maxlength':'3', 'class':'phone', 'prefix':'+1 ( '}),
            forms.TextInput(attrs={'size':'3','maxlength':'3', 'class':'phone', 'prefix':') '}),
            forms.TextInput(attrs={'size':'4','maxlength':'4', 'class':'phone', 'prefix':' - '}),
        ]
        super(USPhoneNumberMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            matches = re.split("\+1 \(([0-9]+)\)-([0-9]+)-([0-9]+)", value)
            if (matches and len(matches) == 5):
            	return [matches[1], matches[2], matches[3]]
        return [None,None,None]

    def value_from_datadict(self, data, files, name):
        values = super(USPhoneNumberMultiWidget, self).value_from_datadict(data, files, name)
        return u'+1 (%s)-%s-%s' % (values[0], values[1], values[2])

class TimeWidget(forms.TimeInput):
    def __init__(self, attrs=None):
        if attrs == None:
            attrs = {}
        attrs['type'] = 'time'
        forms.TimeInput.__init__(self, attrs)

class OpeningHoursMultiWidget(forms.MultiWidget):
    class Media:
        js = ('js/weekly_opening_hours.js',)
    def __init__(self, attrs=None):
        self.template_name = 'widgets/opening_hours.html'
        widgets = [forms.CheckboxInput(attrs={'class': 'time_enabled', 'style': 'visibility: hidden'}),
                   TimeWidget(attrs={'class': 'time', 'value': DEFAULT_OPENING_TIME}),
                   TimeWidget(attrs={'class': 'time', 'value': DEFAULT_CLOSING_TIME, 'prefix': ' to '})]
        super(OpeningHoursMultiWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            return [value.enabled, value.opening_time, value.closing_time]
        return [None,None,None]

    def value_from_datadict(self, data, files, name):
        values = super(OpeningHoursMultiWidget, self).value_from_datadict(data, files, name)
        if values[0]:
             return '%s %s'%(values[1], values[2])
        else:
          return None

def get_widget_attributes(i):
    return {'weekday': WEEKDAYS[i],
            'closed_text': 'closed',                                                  
            'weekday_id': 'opening_hours_weekday_%d'%(i),
            'hours_id': 'opening_hours_times_%d'%(i),
            'style': 'visibility: hidden'}

class WeeklyOpeningHoursMultiWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        self.template_name = 'widgets/weekly_opening_hours.html'
        widgets = []
        for i in range(len(WEEKDAYS)):
            widgets.append(OpeningHoursMultiWidget(attrs=get_widget_attributes(i)))
        super(WeeklyOpeningHoursMultiWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if (isinstance(value, str)):
                v = parse_weekly_opening_hours(value)
            else:
                v = value
            values = []
            widgets = []
            for i in range(len(WEEKDAYS)):
                opening_hours = v.opening_hours[WEEKDAYS[i]]
                values.append(opening_hours)
                attrs = get_widget_attributes(i)
                if opening_hours.enabled:
                    attrs['closed_text'] = ''
                    attrs.pop('style', None)
                widgets.append(OpeningHoursMultiWidget(attrs=attrs))

            super(WeeklyOpeningHoursMultiWidget, self).__init__(widgets, None)
            return values
        return [None, None, None, None, None, None, None]

    def value_from_datadict(self, data, files, name):
        values = super(WeeklyOpeningHoursMultiWidget, self).value_from_datadict(data, files, name)
        str = ''
        for i in range(7):
            str += '(%s %s)'%(WEEKDAYS[i], values[i])
        return str

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class AddResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('resource_name',
                  'org_name',
                  'category',
                  'opening_hours',
                  'phone',
                  'address',
                  'street_number',
                  'street_name',
                  'city',
                  'state',
                  'country',
                  'postal_code',
                  'long',
                  'lat',
                  'url',
                  'notes')
        widgets = {
            'resource_name': forms.TextInput(),
            'org_name': forms.TextInput(),
            'category': forms.Select(),
            'opening_hours': WeeklyOpeningHoursMultiWidget(),
            'phone': USPhoneNumberMultiWidget(),
            'address': forms.TextInput(),
            'street_number': forms.HiddenInput(),
            'street_name': forms.HiddenInput(),
            'city': forms.HiddenInput(),
            'state': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'postal_code': forms.HiddenInput(),
            'long': forms.HiddenInput(),
            'lat': forms.HiddenInput(),
            'url': forms.TextInput(),
            'notes': forms.TextInput()
        }
    resource_name = forms.CharField(max_length=100, required=True)
    org_name = forms.CharField(max_length=100, required=True)
    category = forms.ChoiceField(choices=Resource.CATEGORIES)
    opening_hours = forms.CharField(max_length=512, widget=WeeklyOpeningHoursMultiWidget(), required=False)
    phone = forms.CharField(widget=USPhoneNumberMultiWidget())
  
    address = forms.CharField(max_length=100, required=True)
    street_number = forms.CharField(widget=forms.HiddenInput(),
                                    max_length=100, required=False, disabled=False)
    street_name = forms.CharField(widget=forms.HiddenInput(),
                                  max_length=100, required=False, disabled=False)
    city = forms.CharField(widget=forms.HiddenInput(),
                           max_length=100, required=False, disabled=False)
    state = forms.CharField(widget=forms.HiddenInput(),
                            max_length=100, required=False, disabled=False)
    country = forms.CharField(widget=forms.HiddenInput(),
                              max_length=100, required=False, disabled=False)
    postal_code = forms.CharField(widget=forms.HiddenInput(),
                                  max_length=100, required=False, disabled=False)
    long = forms.DecimalField(widget=forms.HiddenInput(),
                              required=False, disabled=False)
    lat = forms.DecimalField(widget=forms.HiddenInput(),
                             required=False, disabled=False)

    url = forms.URLField(max_length=100, required=False)
    notes = forms.CharField(max_length=250, required=False)
