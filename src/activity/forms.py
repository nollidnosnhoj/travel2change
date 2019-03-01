from django import forms

from .models import Region

class ActivityForm1(forms.Form):
    title = forms.CharField(max_length=100)
    # region = forms.ModelChoiceField(queryset=Region.objects())
    description = forms.CharField(widget=forms.Textarea, max_length=400)

class ActivityForm2(forms.Form):

