from django import forms

from app1.models import Person


class PersonCreateForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
