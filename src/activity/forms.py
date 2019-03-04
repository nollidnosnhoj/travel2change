from django import forms

from .models import Activity, ActivityImage

# Step One (Input Title, Region, and Description)


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


"""
TODO:
- Handle multiple images uploading
"""


# Step Five (Upload Images)
class ImagesActivityForm(forms.ModelForm):
    pass
