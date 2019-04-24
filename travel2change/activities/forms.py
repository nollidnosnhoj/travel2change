from django import forms
from .models import Activity


class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'region', ]


class HighlightsForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['highlights', ]


class RequirementsForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['requirements', ]


class CategoriesTagsForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['categories', 'tags', ]


class PriceForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['price', 'fh_item_id', ]


class LocationForm(forms.ModelForm):
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


class FeaturedPhotoForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['featured_photo', ]
        widget = {
            'featured_photo': forms.ClearableFileInput(attrs={'required': True})
        }


class ConfirmationForm(forms.Form):
    pass


""" Form that corresponds to each step of the activity creation """
ACTIVITY_CREATE_FORMS_LIST = [
    ("1", BasicInfoForm),
    ("2", HighlightsForm),
    ("3", RequirementsForm),
    ("4", CategoriesTagsForm),
    ("5", PriceForm),
    ("6", LocationForm),
    ("7", FeaturedPhotoForm),
    ("8", ConfirmationForm),
]


class PhotoUploadForm(forms.Form):
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'multiple': True
    }))


""" CMS Wizard Form """
class ActivityWizardForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = [
            'approved_time', 'created', 'modified', 'slug',
        ]
