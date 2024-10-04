from django import forms
from django.utils.translation import gettext_lazy as _


class AnalysisForm(forms.Form):
    title = forms.CharField(
        label=_("Title"),
        required=False,
        widget=forms.TextInput()
    )
    
    notes = forms.CharField(
        label=_("Notes"),
        required=False,
        widget=forms.Textarea()
    )