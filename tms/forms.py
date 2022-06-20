from django import forms
from django.forms.models import inlineformset_factory
from .models import Work,User


class Taskform(forms.ModelForm):
    class Meta:
        model = Work
        fields = (
            "app_name",
            "work_name",
            "work_descp"
        )
