from django import forms
from .models import ActivityReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ActivityReview
        fields = ('rating', 'content', 'photo', 'show_name', 'show_email', )
