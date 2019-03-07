from django import forms

from .models import Activity


class RegionActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['region', ]


class TitleActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'price', ]


# Step Two (Input Highlights, Requirements, and Tags)
class AboutActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['highlights', 'requirements', 'tags', ]


# Step Three (Input Location)
class AddressActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['address', ]


# Step Four (Confirm Location is Correct)
class LocationActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['latitude', 'longitude', ]


# { "Step Name" : Form Class }

ACTIVITY_CREATE_FORMS_LIST = [
    ("0", RegionActivityForm),
    ("1", TitleActivityForm),
    ("2", AboutActivityForm),
    ("3", AddressActivityForm),
    ("4", LocationActivityForm),
]
