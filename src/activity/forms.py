from django import forms

from .models import Region, Tag

# Step One (Input Title, Region, and Description)
class ActivityForm1(forms.Form):
    title           = forms.CharField(max_length=100)
    region          = forms.ModelChoiceField(queryset=Region.objects.all())
    description     = forms.CharField(widget=forms.Textarea, max_length=400)

# Step Two (Input Highlights, Requirements, and Tags)
class ActivityForm2(forms.Form):
    highlights      = forms.CharField(widget=forms.Textarea, max_length=400)
    requirements    = forms.CharField(widget=forms.Textarea)
    tags            = forms.ModelMultipleChoiceField(
                        queryset=Tag.objects.all(), 
                        widget=forms.CheckboxSelectMultiple
                    )

# Step Three (Input Location)
class ActivityForm3(forms.Form):
    pass

# Step Four (Confirm Location is Correct)
class ActivityForm4(forms.Form):
    pass

# Step Five ()
class ActivityForm5(forms.Form):
    pass
