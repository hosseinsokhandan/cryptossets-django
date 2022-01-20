from account.models import Info
from django import forms


class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        exclude = ["id", "user"]
