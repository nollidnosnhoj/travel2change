from django import forms
from django.utils.translation import ugettext_lazy as _

from activities.models import Activity

class DisapproveForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(),
        help_text=_('Insert reasons why this activity was not approved.'),
    )

    def send_email(self):
        # send email about disapproval with reason
        pass


class ApproveForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('fb_item_id', )
