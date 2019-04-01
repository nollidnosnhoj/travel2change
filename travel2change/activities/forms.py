from django import forms
from .models import Activity, ActivityReview, Comment


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


class TagsForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['tags', ]


class PriceForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['price', ]


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


""" Form that corresponds to each step of the activity creation """
ACTIVITY_CREATE_FORMS_LIST = [
    ("0", BasicInfoForm),
    ("1", HighlightsForm),
    ("2", RequirementsForm),
    ("3", TagsForm),
    ("4", PriceForm),
    ("5", LocationForm),
    ("6", FeaturedPhotoForm),
]


class ActivityUpdateForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = (
            'title',
            'region',
            'description',
            'highlights',
            'requirements',
            'tags',
            'featured_photo',
            'price',
            'address',
            'latitude',
            'longitude',
        )
        widgets = {
            'latitude': forms.TextInput(attrs={
                'id': 'lat_field',
            }),
            'longitude': forms.TextInput(attrs={
                'id': 'lng_field',
            })
        }


class PhotoUploadForm(forms.Form):
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'multiple': True
    }))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ActivityReview
        fields = ('rating', 'content', )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


""" CMS Wizard Form """
class ActivityWizardForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = [
            'slug', 'review_count', 'created', 'modified',
        ]
