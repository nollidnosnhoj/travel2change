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


# Step Four (Confirm Location is Correct)
class LocationActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['address', 'latitude', 'longitude', ]
        widgets = {
            'latitude': forms.HiddenInput(attrs={
                'id': 'lat_field'
            }),
            'longitude': forms.HiddenInput(attrs={
                'id': 'lng_field'
            })
        }


# { "Step Name" : Form Class }

ACTIVITY_CREATE_FORMS_LIST = [
    ("0", RegionActivityForm),
    ("1", TitleActivityForm),
    ("2", AboutActivityForm),
    ("3", LocationActivityForm),
]
