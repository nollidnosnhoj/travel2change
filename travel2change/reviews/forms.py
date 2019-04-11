from django import forms
from .models import ActivityReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ActivityReview
        fields = ('rating', 'content', 'photo', 'show_name', 'show_email', )
        widgets = {'rating': forms.NumberInput(attrs={
            'id': 'input-rating',
            'stars': len(ActivityReview.RATING_CHOICES),
            'min': 0,
            'max': len(ActivityReview.RATING_CHOICES),
            'step': 1,
        })}
