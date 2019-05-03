from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'content', 'photo', 'show_name', 'show_email', )
        # the id change is to work with the rating jquery plugin
        widgets = {'rating': forms.NumberInput(attrs={'id': 'input-rating'})}
